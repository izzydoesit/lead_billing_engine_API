from fastapi import APIRouter
from uuid import UUID
from typing import Optional, List, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
import app.models as models
from app.crud.leads_service import calculate_action_cost
from app.crud.billing_report_service import (
    is_duplicate_action,
    calculate_totals_by_product,
)

router = APIRouter()


# FIXME: TODO: -----> THIS ENDPOINT SHOULD TAKE DATE RANGES AS QUERY PARAMETERS!!!!
@router.get("/billing-reports/")
async def generate_billing_report(
    customer_id: int, db: Annotated[AsyncSession, Depends(get_async_session)]
):
    report = dict()
    # fetch customer record
    customer = (
        db.query(models.Customers)
        .filter(models.Customers.customer_id == customer_id)
        .first()
    )
    #  populate report with customer details
    report["customer_id"] = customer.customer_id
    report["customer_name"] = customer.name
    report["customer_email"] = customer.email
    # fetch customer actions
    customer_actions = (
        db.query(models.Actions).filter(models.Actions.customer_id == customer_id).all()
    )
    # populate report with empty actions list
    report["actions"] = []  # all actions that have been processed
    total_amount = 0.0
    billing_cap = 100.0
    savings_amount = 0.0
    product_id_actions_list_map = {}  # add all actions after checking if duped

    # go through each action and...
    for action in customer_actions:
        # calculate + assign a value to cost_amount field
        action.cost_amount = calculate_action_cost(action.lead_type, action.action_type)
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
                # add cost_amount to total_amount
                total_amount += action.cost_amount

            # add action to product_id_actions_list_map list
            product_id_actions_list_map[action.product_id].append(action)
        else:
            # else set duplicate field to False
            action = set_duplicate_fields(action, False)
            # add cost_amount to total_amount
            total_amount += action.cost_amount
            # create list in product_id_actions_list_map with action
            product_id_actions_list_map[action.product_id] = [action]

        # add the action to the report
        report["actions"].append(action)

    # calculate totals by product + add to report
    report["totals_by_product"] = models.BillingReports.totals_by_product(
        calculate_totals_by_product(product_id_actions_list_map)
    )
    # add total amount with cap to report
    if total_amount > billing_cap:
        report["total_amount"] = billing_cap
        savings_amount += total_amount - billing_cap
    else:
        report["total_amount"] = total_amount
    # add savings amount to report
    report["savings_amount"] = savings_amount
    # save the report to the database
    db_report = models.BillingReports(**report)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    return report.json()
