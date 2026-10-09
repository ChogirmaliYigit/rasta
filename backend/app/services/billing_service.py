from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from decimal import Decimal
from app.models.billing import BillingLedger
from app.models.order import Order
from app.schemas.billing import CreditPaymentCreate, BillingStatementResponse, BillingEntryResponse
from app.schemas.common import TransactionType

async def get_current_balance(db: AsyncSession, org_id: UUID) -> Decimal:
    stmt = select(BillingLedger).where(BillingLedger.organization_id == org_id).order_by(BillingLedger.created_at.desc()).limit(1)
    entry = await db.scalar(stmt)
    return entry.balance_after if entry else Decimal("0.00")

async def record_platform_fee(db: AsyncSession, order: Order) -> BillingLedger:
    from sqlalchemy.orm import selectinload
    from app.models.organization import Branch
    branch = await db.scalar(select(Branch).where(Branch.id == order.wholesaler_branch_id))
    
    current_balance = await get_current_balance(db, branch.organization_id)
    fee = order.final_amount * Decimal("0.01")
    new_balance = current_balance + fee
    
    entry = BillingLedger(
        organization_id=branch.organization_id,
        transaction_type=TransactionType.DEBIT_FEE,
        amount=fee,
        balance_after=new_balance,
        reference_order_id=order.id,
        description=f"Platform fee for order {order.order_number}"
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry

async def record_credit_payment(db: AsyncSession, org_id: UUID, data: CreditPaymentCreate) -> BillingLedger:
    current_balance = await get_current_balance(db, org_id)
    new_balance = current_balance - data.amount
    
    entry = BillingLedger(
        organization_id=org_id,
        transaction_type=TransactionType.CREDIT_PAYMENT,
        amount=data.amount,
        balance_after=new_balance,
        description=data.description
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry

async def get_billing_statement(db: AsyncSession, org_id: UUID, page: int, per_page: int) -> BillingStatementResponse:
    current_balance = await get_current_balance(db, org_id)
    query = select(BillingLedger).where(BillingLedger.organization_id == org_id).order_by(BillingLedger.created_at.desc())
    result = await db.execute(query.offset((page - 1) * per_page).limit(per_page))
    entries = result.scalars().all()
    return BillingStatementResponse(
        current_balance=current_balance,
        entries=[BillingEntryResponse.model_validate(e) for e in entries]
    )

async def check_credit_limit(db: AsyncSession, org_id: UUID, credit_limit: Decimal) -> bool:
    bal = await get_current_balance(db, org_id)
    return bal > credit_limit
