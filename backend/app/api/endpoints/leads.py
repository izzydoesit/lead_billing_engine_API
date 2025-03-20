from http.client import HTTPResponse
from typing import List, Optional, Union, Annotated
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_async_session
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
from app.crud import calculate_action_cost
from app.shared.billing_lead_types import LeadSources

router = APIRouter()


@router.get("/leads", response_model=Lead)
async def get_leads(
    db: AsyncSession = Depends(get_async_session),
    customer_id: str = None,
    product_id: str = None,
    lead_type: LeadSources = None,
):
    result = None
    sql_query = "SELECT * FROM leads"
    if customer_id or product_id or lead_type:
        where_clause = " WHERE leads."

        sql_query += f"WHERE leads.customer_id EQUALS ${customer_id}"
    elif lead_type and not customer_id:
        result = await db.execute(
            select(models.Leads).where(models.Leads.lead_type == lead_type)
        )
    elif customer_id and lead_type:
        result = await db.execute(
            select(models.Leads).where(
                Leads.customer_id == customer_id and models.Leads.lead_type == lead_type
            )
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid query parameters")

    result = await db.execute(select(models.Lead)).all()

    if result is None:
        raise HTTPException(status_code=404, detail="Leads not found")
    return result


@router.get("/leads/{lead_id}", response_model=Lead)
async def get_one_lead(lead_id: int, db: AsyncSession = Depends(get_async_session)):
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
    leads_list: List[LeadCreate], db: AsyncSession = Depends(get_async_session)
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
