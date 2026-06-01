from datetime import date
from typing import Annotated, Literal, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.transaction_repo import TransactionRepository
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionUpdate

router = APIRouter(prefix="/transactions", tags=["transactions"])


def get_transaction_repo(session: Annotated[AsyncSession, Depends(get_db)]) -> TransactionRepository:
    return TransactionRepository(session)


TransactionRepoDep = Annotated[TransactionRepository, Depends(get_transaction_repo)]


@router.get("/", response_model=list[TransactionResponse])
async def list_transactions(
    repo: TransactionRepoDep,
    type: Optional[Literal["income", "expense"]] = Query(None),
    category_id: Optional[int] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> list[TransactionResponse]:
    return await repo.get_all(
        type=type,
        category_id=category_id,
        date_from=date_from,
        date_to=date_to,
        page=page,
        size=size,
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: int, repo: TransactionRepoDep) -> TransactionResponse:
    return await repo.get_by_id(transaction_id)


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(body: TransactionCreate, repo: TransactionRepoDep) -> TransactionResponse:
    return await repo.create(body)


@router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int, body: TransactionUpdate, repo: TransactionRepoDep
) -> TransactionResponse:
    return await repo.update(transaction_id, body)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: int, repo: TransactionRepoDep) -> None:
    await repo.delete(transaction_id)
