from fastapi import APIRouter, HTTPException, Depends, Query
from datetime import datetime
from uuid import uuid4
from collections import defaultdict
import logging
from typing import Optional, List, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.future import select
from collections import defaultdict
from sqlalchemy.orm import selectinload
from app.core.database import get_async_session

from app.models import (
    Customer as CustomerModel,
    Action as ActionModel,
    BillingReport as BillingReportModel,
)
from app.crud.leads_service import calculate_action_value
from app.schemas import (
    BillingReport as BillingReportSchema,
    BillingReportItem as BillingReportItemSchema,
)
from app.crud.billing_report_service import (
    is_duplicate_action,
    calculate_totals_by_product,
)
from app.shared import (
    LEAD_TYPE_BASE_VALUES,
    LEAD_ACTION_COSTS,
    ENGAGEMENT_MULTIPLIERS,
    BILLING_CAP,
)

router = APIRouter()
logger = logging.getLogger(__name__)


def calculate_action_value(
    lead_type: str, action_type: str, engagement_level: str
) -> float:
    base_value = LEAD_TYPE_BASE_VALUES.get(lead_type, 0)
    action_value = LEAD_ACTION_COSTS.get(lead_type, {}).get(action_type, 0)
    engagement_multiplier = ENGAGEMENT_MULTIPLIERS.get(engagement_level, 1)
    return base_value + (action_value * engagement_multiplier)


def format_report(
    report: BillingReportSchema, customer_name: str, customer_email: str
) -> str:
    report_str = f"### **Detailed Billing Breakdown**\n\n"
    report_str += f"#### **B2B Partner Company: `{customer_name}`**\n"
    report_str += f"**End Customer Email:** `{customer_email}`\n\n"
    report_str += "| **Customer Email** | **Associated Product** | **Lead Type**    | **Action Type**    | **Engagement Level** | **Amount (USD)** | **Duplicate**                 | **Status**                 |\n"
    report_str += "|--------------------|------------------------|-------------------|--------------------|-----------------------|-------------------|-------------------------------|----------------------------|\n"

    for item in report.items:
        report_str += f"| `{item.customer_email}`   | `{item.associated_product}`          | {item.lead_type}     | {item.action_type}    | {item.engagement_level}                  | ${item.amount:.2f}            | {'Yes' if item.duplicate else 'No'}                            | {item.status}                     |\n"

    report_str += "\n"
    for product, subtotal in report.product_subtotals.items():
        report_str += f"**Subtotal for `{product}`:** ${subtotal:.2f}  \n"

    report_str += f"\n**Total Billed Amount:** ${report.total_billed_amount:.2f}  \n"
    report_str += (
        f"**Total Savings from Duplicates and Caps:** ${report.total_savings:.2f}\n\n"
    )
    report_str += "*Explanation: Duplicate actions have been detected and not billed again, resulting in significant savings."
    if report.total_billed_amount == BILLING_CAP:
        report_str += (
            " The total billed amount has reached the billing cap of $100.00.*\n\n"
        )
    else:
        report_str += (
            " The total billed amount is below the billing cap of $100.00.*\n\n"
        )

    return report_str


@router.get("/billingReports", response_model=BillingReportSchema)
async def generate_billing_report(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    customer_id: str,
    start_date: Optional[datetime] = Query(
        None, description="Start date for the billing report"
    ),
    end_date: Optional[datetime] = Query(
        None, description="End date for the billing report"
    ),
):
    try:
        # Fetch the customer details
        customer_query = select(CustomerModel).where(CustomerModel.id == customer_id)
        customer_result = await db.execute(customer_query)
        customer = customer_result.unique().scalar_one_or_none()

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        customer_name = customer.name
        customer_email = customer.email

        query = select(ActionModel).where(ActionModel.customer_id == customer_id)
        if start_date:
            query = query.where(ActionModel.created_at >= start_date)
        if end_date:
            query = query.where(ActionModel.created_at <= end_date)

        result = await db.execute(query)
        actions = result.unique().scalars().all()

        if not actions:
            raise HTTPException(
                status_code=404,
                detail="No actions found for the given customer and date range",
            )

        total_billed_amount = 0.0
        total_savings = 0.0
        report_items = []
        product_subtotals = defaultdict(float)
        seen_actions = set()

        for action in actions:
            lead_amount = LEAD_TYPE_BASE_VALUES.get(action.lead_type, 0)

            action_value = calculate_action_value(
                action.lead_type, action.action_type, action.engagement_level
            )
            lead_amount += action_value

            total_billed_amount += lead_amount
            report_items.append(
                BillingReportItemSchema(
                    id=str(uuid4()),
                    lead_id=action.lead_id,
                    product_id=action.product_id,
                    customer_id=action.customer_id,
                    lead_type=action.lead_type,
                    total_billed_amount=total_billed_amount,
                    customer_email=customer_email,
                    associated_product=action.product.name if action.product else None,
                    action_type=action.action_type,
                    engagement_level=action.engagement_level,
                    amount=action_value,
                    duplicate=action.is_duplicate or False,
                    status=action.status or "pending",
                    actions=[
                        {
                            "action_type": action.action_type,
                            "engagement_level": action.engagement_level,
                            "value": calculate_action_value(
                                action.lead_type,
                                action.action_type,
                                action.engagement_level,
                            ),
                        }
                    ],
                )
            )

        # Calculate product subtotals
        product_subtotals = defaultdict(float)
        for item in report_items:
            if item.associated_product:
                product_subtotals[item.associated_product] += item.amount

        billing_report = BillingReportSchema(
            id=str(uuid4()),
            customer_id=customer_id,
            total_billed_amount=total_billed_amount,
            items=report_items,
            product_subtotals=dict(product_subtotals),
        )

        return billing_report

    except SQLAlchemyError as e:
        logging.error(f"Database query error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database query error")

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error")

    report = dict()
    # fetch customer record
    # customer = (
    #     db.query(models.Customers)
    #     .filter(models.Customers.customer_id == customer_id)
    #     .first()
    # )
    #  populate report with customer details
    report["customer_id"] = customer.customer_id
    report["customer_name"] = customer.name
    report["customer_email"] = customer.email
    # fetch customer actions
    customer_actions = (
        db.query(ActionModel).filter(ActionModel.customer_id == customer_id).all()
    )
    # populate report with empty actions list
    report["actions"] = []  # all actions that have been processed
    total_billed_amount = 0.0
    billing_cap = 100.0
    savings_amount = 0.0
    product_id_actions_list_map = {}  # add all actions after checking if duped

    # go through each action and...
    for action in customer_actions:
        # calculate + assign a value to cost_amount field
        action.cost_amount = calculate_action_value(
            action.lead_type, action.action_type
        )
        # if we've seen this product_id before, check for duplicates based on identical product_id, lead_type and action_type
        if action.product_id in product_id_actions_list_map:
            # if we have a duplicate:
            if is_duplicate_action(
                action, product_id_actions_list_map[action.product_id]
            ):
                # set duplicate fields to True
                action = set_duplicate_fields(action, True)
                # add cost_amount to savings_amount
                savings_amount += action.cost_amount
            else:
                # else set duplicate field to False
                action = set_duplicate_fields(action, False)
                # add cost_amount to total_billed_amount
                total_billed_amount += action.cost_amount

            # add action to product_id_actions_list_map list
            product_id_actions_list_map[action.product_id].append(action)
        else:
            # else set duplicate field to False
            action = set_duplicate_fields(action, False)
            # add cost_amount to total_billed_amount
            total_billed_amount += action.cost_amount
            # create list in product_id_actions_list_map with action
            product_id_actions_list_map[action.product_id] = [action]

        # add the action to the report
        report["actions"].append(action)

    # calculate totals by product + add to report
    report["totals_by_product"] = BillingReportModel.totals_by_product(
        calculate_totals_by_product(product_id_actions_list_map)
    )
    # add total amount with cap to report
    if total_billed_amount > billing_cap:
        report["total_billed_amount"] = billing_cap
        savings_amount += total_billed_amount - billing_cap
    else:
        report["total_billed_amount"] = total_billed_amount
    # add savings amount to report
    report["savings_amount"] = savings_amount
    # save the report to the database
    db_report = BillingReportModel(**report)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    return report.json()
