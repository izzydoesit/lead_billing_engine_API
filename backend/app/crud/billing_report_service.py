from app.schemas.base import BillingReportCreate, BillingReport, Action
from decimal import Decimal


async def get_billing_report():
    pass


def calculate_totals_by_product(product_id_actions_list_map: dict) -> list[dict]:
    totals_by_product: list = []
    for product_id, actions_list in product_id_actions_list_map:
        total_product_cost: Decimal = 0.0
        for action in actions_list:
            total_product_cost += action.cost_amount if not action.is_duplicate else 0.0
        totals_by_product.append({product_id: total_product_cost})

    return totals_by_product


def is_duplicate_action(current_action, processed_product_actions: list) -> bool:
    for processed_action in processed_product_actions:
        if (
            current_action.product_id == processed_action.product_id
            and current_action.lead_type == processed_action.lead_type
            and current_action.action_type == processed_action.action_type
        ):
            return True
    return False


def set_duplicate_fields(action, is_duplicate):
    action.is_duplicate = is_duplicate
    action.status = "Not Billed (Duplicate)" if is_duplicate else "Billed"
    return action
