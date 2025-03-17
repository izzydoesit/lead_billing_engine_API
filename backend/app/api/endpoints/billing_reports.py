from fastapi import APIRouter
from database import db_dependency
import models
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List
from .leads import ActionBase

router = APIRouter()

class BillingReportBase(BaseModel):
    billing_report_id: UUID
    billing_date: str
    customer_name: str
    customer_email: str
    customer_id: UUID
    lead_actions: List[ActionBase] = []
    total_amount: float
    savings_amount: Optional[float] = 0.0

lead_action_costs = {
    "Website Visit": {
        "Visit": 1,
        "Click": 2,
        "Download": 3,
        "Form Submit": 5,
        "Purchase": 10
    },
    "Social Media": {
        "Like": 2,
        "Follow": 3,
        "Share": 5,
        "Comment": 7,
        "Repost": 10
    },
    "Email Campaign": {
        "Open": 1,
        "Click": 15,
        "Unsubscribe": 5
    },
    "Referral": {
        "Signup": 20,
        "Purchase": 50
    },
    "Event": {
        "Attend": 2,
    },
    "Webinar": {
        "Register": 5,
        "Attend": 10,
        "Follow-up": 5
    },
    "Demo Request": {
        "Submission": 10,
        "Follow-up": 5
    },
    "Trade Show": {
        "Visit": 5,
        "Follow-up": 10
    },
    "Conference": {
        "Attendance": 15,
        "Follow-up": 5
    },
    "Newsletter": {
        "Open": 1,
        "Click": 5
    },
    "Feedback": {
        "Submission": 10
    }
}

def calculate_action_cost(lead_type, action_type):
    if action_type in lead_action_costs:
        action_costs = lead_action_costs[lead_type]
        if isinstance(action_costs, dict):
            cost = action_costs.get(action_type, 0)
        return cost
    return 0

def calculate_totals_by_product(product_actions: dict):
    totals_by_product = {}

    for product in product_actions:
        total_amount = 0.0
        for action in product_actions[product]:
            total_amount += action.cost_amount
        totals_by_product[product] = total_amount

    return totals_by_product

def is_duplicate_action(action, product_actions_map):
    for existing_action in product_actions_map[action.product_id]:
        if action.lead_type == existing_action.lead_type and action.action_type == existing_action.action_type:
            return True
    return False

def set_duplicate_fields(action, is_duplicate):
    action.is_duplicate = is_duplicate
    action.status = "Not Billed (Duplicate)" if is_duplicate else "Billed"
    return action

@router.get("/billing-reports/{customer_id}")
async def generate_billing_report(customer_id: int, db: db_dependency):
    report = dict()
    # fetch customer record
    customer = db.query(models.Customers).filter(models.Customers.customer_id == customer_id).first()
    #  populate report with customer details
    report["customer_id"] = customer.customer_id
    report["customer_name"] = customer.name
    report["customer_email"] = customer.email
    # fetch customer actions
    customer_actions = db.query(models.Actions).filter(models.Actions.customer_id == customer_id).all()
    # populate report with empty actions list
    report["actions"] = [] # all actions that have been processed
    total_amount = 0.0
    billing_cap = 100.0
    savings_amount = 0.0
    product_actions_map = {} # add all actions after checking if duped

    # go through each action and... 
    for action in customer_actions:
        # calculate + assign a value to cost_amount field
        action.cost_amount = calculate_action_cost(action.lead_type, action.action_type)
        # dedupe actions based on identical product_id, lead_type and action_type
        # if we've seen this product_id before, check for duplicates
        if action.product_id in product_actions_map:
            # if we have a duplicate:
            if is_duplicate_action(action, product_actions_map):
                # set duplicate fields to True
                action = set_duplicate_fields(action, True)
                # add cost_amount to savings_amount
                savings_amount += action.cost_amount
            else:
                # else set duplicate field to False
                action = set_duplicate_fields(action, False)
                # add cost_amount to total_amount
                total_amount += action.cost_amount

            # add action to product_actions_map list
            product_actions_map[action.product_id].append(action)
        else:
            # else set duplicate field to False
            set_duplicate_fields(action, False)
            # add cost_amount to total_amount
            total_amount += action.cost_amount
            # create list in product_actions_map with action
            product_actions_map[action.product_id] = [action]

        # add the action to the report
        report["actions"].append(action)
    
    # calculate totals by product + add to report
    report["totals_by_product"] = calculate_totals_by_product(product_actions_map)
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