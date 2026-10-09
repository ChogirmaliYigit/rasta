from __future__ import annotations
from fastapi import APIRouter, Depends
from uuid import UUID
from app.dependencies import get_db
from app.dependencies import get_current_user, CurrentUser, RoleChecker
from app.schemas.billing import BillingStatementResponse, CreditPaymentCreate, BillingEntryResponse
from app.services import billing_service

router = APIRouter(prefix="/billing", tags=["billing"])

@router.get("/statement", response_model=BillingStatementResponse)
async def get_statement(page: int = 1, per_page: int = 50, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    return await billing_service.get_billing_statement(db, current_user.organization_id, page, per_page)

@router.get("/balance")
async def get_balance(db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    bal = await billing_service.get_current_balance(db, current_user.organization_id)
    return {"current_balance": bal}

@router.post("/payment", response_model=BillingEntryResponse)
async def make_payment(org_id: UUID, data: CreditPaymentCreate, db: AsyncSession = Depends(get_db), current_user: CurrentUser = Depends(RoleChecker(["SUPERADMIN"]))):
    return await billing_service.record_credit_payment(db, org_id, data)
