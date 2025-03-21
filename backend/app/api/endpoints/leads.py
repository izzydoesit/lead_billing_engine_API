from http.client import HTTPResponse
from typing import List, Optional, Union, Annotated
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging
from app.core.database import get_async_session
import app.models as models
from app.schemas import (
    CustomerCreate,
    Customer,
    Lead,
    LeadCreate,
    ProductCreate,
    Product,
    LeadCreate,
    ActionCreate,
    Action,
)
from app.crud import calculate_action_value
from app.crud.leads_service import (
    save_lead_in_database,
    save_action_in_database,
)
from app.shared import LeadTypes, LEAD_ACTION_COSTS

router = APIRouter()


@router.get("/leads", response_model=Lead)
async def get_leads(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    customer_id: Optional[str] = Query(None, description="Filter by customer ID"),
    product_id: Optional[str] = Query(None, description="Filter by product ID"),
    lead_type: Optional[LeadTypes] = Query(None, description="Filter by lead type"),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(Lead)

        if customer_id:
            query = query.where(Lead.customer_id == customer_id)
        if product_id:
            query = query.where(Lead.product_id == product_id)
        if lead_type:
            query = query.where(Lead.lead_type == lead_type)

        result = await session.execute(query)
        leads = result.scalars().all()

        return leads

    except SQLAlchemyError as e:
        logging.error(f"Database query error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database query error")

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error")


@router.get("/leads/{lead_id}", response_model=Lead)
async def get_one_lead(
    lead_id: int, db: Annotated[AsyncSession, Depends(get_async_session)]
):
    # async with AsyncSessionLocal() as db:
    #     result = await db.execute(select(Leads)).where(Leads.lead_id == lead_id).first()
    #     if result is None:
    #         raise HTTPException(status_code=404, detail="Lead not found")
    #     return result

    # try:
    #     result = await session.get(Leads, lead_id)
    #     if result is None:
    #         raise NoResultFound
    #     return result
    # except NoResultFound:
    #     raise HTTPException(status_code=404, detail="Item not found", headers={"X-Error": "Not-Found"})

    result = await db.get(models.Lead, lead_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return result


@router.post("/leads/", status_code=201)
async def create_lead(
    leads_list: List[LeadCreate],
    db: Annotated[AsyncSession, Depends(get_async_session)],
):
    for lead_data in leads_list:
        save_lead_in_database(lead_data, db)

        lead_actions: List[ActionCreate] = lead_data.actions

        for action_data in lead_actions:
            # NOTE: db_action = Action(**action.dict())
            calculated_lead_action_value = calculate_action_value(
                source=lead_data.lead_type,
                result=action_data.action_type,
                quality=action_data.engagement_type,
            )
            action_data.cost_amount = calculated_lead_action_value

            save_action_in_database(action_data, db)

    return HTTPResponse(201)


@router.post("/customers/", response_model=Customer, status_code=201)
async def create_customer(
    customer_data: CustomerCreate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
) -> models.Customer:
    db_customer = models.Customer(name=customer_data.name, email=customer_data.email)
    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer


@router.post("/products/", response_model=Product, status_code=201)
async def create_product(
    product_data: ProductCreate, db: Annotated[AsyncSession, Depends(get_async_session)]
):
    db_product = models.Product(**product_data.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product
