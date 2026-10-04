from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.book import Book
from app.schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=list[BookResponse])
async def list_books(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """Получить список книг с пагинацией."""
    query = select(Book).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Получить книгу по ID."""
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена",
        )
    return book


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_in: BookCreate,
    db: AsyncSession = Depends(get_db),
):
    """Создать новую книгу."""
    book = Book(**book_in.model_dump())
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book


@router.patch("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book_in: BookUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Обновить существующую книгу."""
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена",
        )

    update_data = book_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)

    await db.commit()
    await db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Удалить книгу по ID."""
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена",
        )

    await db.delete(book)
    await db.commit()
