from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.schemas import LeadCreate, Lead, Action, ActionCreate
from app.core.database import get_async_session
import app.models as models
from app.shared import LEAD_ACTION_COSTS


def calculate_action_value(lead_type, action_type, engagement_level):

    if result in LEAD_ACTION_COSTS.get(lead_type, {}):
        action_costs = LEAD_ACTION_COSTS[source]
        if isinstance(action_costs, dict):
            cost = action_costs.get(result, 0)
        return cost
    return 0


# LEADS


# FIXME: this function is not implemented yet
async def get_leads_from_db():
    pass


async def save_lead_in_database(
    lead: LeadCreate, db: Annotated[AsyncSession, Depends(get_async_session)]
):
    db_lead = models.Lead(
        id=lead.lead_id,
        customer_id=lead.customer_id,
        product_id=lead.product_id,
        lead_type=lead.lead_type,
        created_at=lead.created_at,
    )
    try:
        db.add(db_lead)
        await db.commit()
        await db.refresh(db_lead)
    except SQLAlchemyError as e:
        error = str(e.__cause__)
        await db.rollback()
        raise RuntimeError(error) from e
    finally:
        return db_lead


async def save_action_in_database(
    action: ActionCreate, db: Annotated[AsyncSession, Depends(get_async_session)]
):
    db_action = models.Action(
        id=UUID(),
        lead_id=action.lead_id,
        customer_id=action.customer_id,
        product_id=action.product_id,
        lead_type=action.lead_type,
        action_type=action.action_type,
        engagement_level=action.engagement_level,
        created_at=action.created_at,
        cost_amount=action.cost_amount,
    )
    try:
        db.add(db_action)
        await db.commit()
        await db.refresh(db_action)
    except SQLAlchemyError as e:
        error = str(e.__cause__)
        await db.rollback()
        raise RuntimeError(error) from e
    finally:
        return db_action


async def get_lead_by_id(id, db: Annotated[AsyncSession, Depends(get_async_session)]):
    result = await db.get(models.Lead, id)
    if result is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return result


async def get_leads_by_lead_type(lead_type):
    pass


async def get_leads_by_customer_id(customer_id):
    pass


async def get_leads_by_product_id(product_id):
    pass


async def get_action_by_id(id):
    pass


async def get_actions():
    pass


# ACTIONS
async def get_actions_by_lead_id():
    pass


async def get_actions_by_customer_id(customer_id):
    pass


async def get_actions_by_product_id(product_id):
    pass


async def get_actions_by_lead_id(lead_id):
    pass
