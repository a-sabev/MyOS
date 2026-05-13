from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
from decimal import Decimal
from app.finance.models import TransactionType

class CategoryCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        description="Category name",
        examples=["Groceries"],
    )

class CategoryResponse(BaseModel):
    id: int
    name: str
    is_default: bool
    model_config = ConfigDict(from_attributes=True)

class TransactionCreate(BaseModel):
    category_id: int = Field(gt=0, description="ID of an existing category")
    amount: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
        description="Transaction amount, must be positive",
    )
    type: TransactionType
    transaction_date: date = Field(description="Date the transaction occurred")
    notes: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional notes about the transaction",
    )

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    amount: Decimal
    type: TransactionType
    transaction_date: date
    notes: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class BudgetCreate(BaseModel):
    category_id: int = Field(gt=0, description="ID of an existing category")
    amount: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
        description="Budget limit for the month, must be positive",
    )
    month: date = Field(description="First day of the budget month (e.g. 2025-05-01)")

class BudgetResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    amount: Decimal
    month: date
    model_config = ConfigDict(from_attributes=True)
