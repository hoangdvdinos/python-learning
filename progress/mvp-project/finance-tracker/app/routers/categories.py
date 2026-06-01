from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.category_repo import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


def get_category_repo(session: Annotated[AsyncSession, Depends(get_db)]) -> CategoryRepository:
    return CategoryRepository(session)


CategoryRepoDep = Annotated[CategoryRepository, Depends(get_category_repo)]


@router.get("/", response_model=list[CategoryResponse])
async def list_categories(repo: CategoryRepoDep) -> list[CategoryResponse]:
    return await repo.get_all()


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, repo: CategoryRepoDep) -> CategoryResponse:
    return await repo.get_by_id(category_id)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(body: CategoryCreate, repo: CategoryRepoDep) -> CategoryResponse:
    return await repo.create(body)


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int, body: CategoryUpdate, repo: CategoryRepoDep
) -> CategoryResponse:
    return await repo.update(category_id, body)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, repo: CategoryRepoDep) -> None:
    await repo.delete(category_id)
