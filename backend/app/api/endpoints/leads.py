from http.client import HTTPResponse
from typing import List, Optional, Union, Annotated
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app.core.database import get_async_session
from app.models import (
    Lead as LeadModel,
    Customer as CustomerModel,
    Product as ProductModel,
)
from app.schemas import (
    CustomerCreate,
    Customer as CustomerSchema,
    LeadCreate,
    Lead as LeadSchema,
    ProductCreate,
    Product as ProductSchema,
    ActionCreate,
    Action as ActionSchema,
)
from app.crud import calculate_action_value
from app.crud.leads_service import (
    save_lead_in_database,
    save_action_in_database,
)
from app.shared import LeadTypes, LEAD_ACTION_COSTS
from app.shared.utils import to_dict

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/leads", response_model=List[LeadSchema])
async def get_leads(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    customer_id: Optional[str] = Query(None, description="Filter by customer ID"),
    product_id: Optional[str] = Query(None, description="Filter by product ID"),
    lead_type: Optional[LeadTypes] = Query(None, description="Filter by lead type"),
):
    try:
        query = select(LeadModel).options(
            selectinload(LeadModel.customer),
            selectinload(LeadModel.product),
            selectinload(LeadModel.actions),
        )

        if customer_id:
            query = query.where(LeadModel.customer_id == customer_id)
        if product_id:
            query = query.where(LeadModel.product_id == product_id)
        if lead_type:
            query = query.where(LeadModel.lead_type == lead_type)

        logger.info(f"~~**~~ GET /leads querying database... QUERY: {query}")
        result = await db.execute(query)
        leads = result.scalars().all()
        logger.info(f"~~**~~ GET /leads finished querying db. RESULT: {leads}")

        return leads

    except SQLAlchemyError as e:
        logger.error(f"Database query error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database query error")

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error")


@router.get("/leads/{lead_id}", response_model=LeadSchema)
async def get_one_lead(
    lead_id: str, db: Annotated[AsyncSession, Depends(get_async_session)]
):
    try:
        logger.info(f"~~**~~ GET /leads/{lead_id} querying database...")
        query = (
            select(LeadModel)
            .options(
                selectinload(LeadModel.customer),
                selectinload(LeadModel.product),
                selectinload(LeadModel.actions),
            )
            .where(LeadModel.id == lead_id)
        )
        result = await db.execute(query)
        lead_db = result.scalar_one()
        logger.info(
            f"~~**~~ GET /leads/{lead_id} finished querying db. RESULT: {lead_db}"
        )

        if lead_db is None:
            raise HTTPException(
                status_code=404,
                detail="Lead not found",
                headers={"X-Error": "Not-Found"},
            )

        lead_dict = to_dict(lead_db)
        logger.info(f"~~**~~ Lead object: {lead_dict}")

        return LeadSchema.from_orm(lead_db)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error")


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
                lead_type=lead_data.lead_type,
                action_type=action_data.action_type,
                engagement_level=action_data.engagement_level,
            )
            action_data.cost_amount = calculated_lead_action_value

            save_action_in_database(action_data, db)

    return HTTPResponse(201)


@router.post("/customers/", response_model=CustomerSchema, status_code=201)
async def create_customer(
    customer_data: CustomerCreate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
) -> CustomerModel:
    db_customer = CustomerModel(name=customer_data.name, email=customer_data.email)
    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer


@router.post("/products/", response_model=ProductSchema, status_code=201)
async def create_product(
    product_data: ProductCreate, db: Annotated[AsyncSession, Depends(get_async_session)]
):
    db_product = ProductModel(**product_data.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product
