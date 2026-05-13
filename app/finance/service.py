from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, desc
from app.finance.models import Category, Transaction, Budget, TransactionType
from app.finance.schemas import CategoryCreate, TransactionCreate, BudgetCreate
from app.exceptions import NotFoundError, DuplicateError


async def create_category(db: AsyncSession, user_id: int, category_data: CategoryCreate) -> Category:
    result = await db.execute(select(Category).where(
        Category.name == category_data.name,
        Category.user_id == user_id
        )
    )
    existing_category = result.scalar_one_or_none()
    
    if existing_category:
        raise DuplicateError("Category already exists")
    
    category = Category(
        user_id=user_id,
        name=category_data.name
    )
    
    db.add(category)
    await db.flush()
    await db.refresh(category)
    return category

async def get_categories(db: AsyncSession, user_id: int) -> list[Category]:
    result = await db.execute(select(Category).where(
        or_(Category.user_id == user_id, Category.is_default.is_(True))
        )
    )
    return list(result.scalars().all())

async def create_transaction(db: AsyncSession, user_id: int, transaction_data: TransactionCreate) -> Transaction:
    category = await _get_category_or_raise(db, transaction_data.category_id, user_id)
    
    transaction = Transaction(
        user_id=user_id,
        category_id=transaction_data.category_id,
        amount=transaction_data.amount,
        type=transaction_data.type,
        transaction_date=transaction_data.transaction_date,
        notes=transaction_data.notes
    )
    
    db.add(transaction)
    await db.flush()
    await db.refresh(transaction)
    return transaction

async def get_transactions(db: AsyncSession, user_id: int) -> list[Transaction]:
    result = await db.execute(
        select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(desc(Transaction.transaction_date))
    )
    return list(result.scalars().all())

async def update_transaction(db: AsyncSession, user_id: int, transaction_id: int, transaction_data: TransactionCreate) -> Transaction:
    result = await db.execute(select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        )
    )

    transaction = result.scalar_one_or_none()

    if not transaction:
        raise NotFoundError("Transaction not found")

    await _get_category_or_raise(db, transaction_data.category_id, user_id)
    
    transaction.category_id = transaction_data.category_id
    transaction.amount = transaction_data.amount
    transaction.type = transaction_data.type
    transaction.transaction_date = transaction_data.transaction_date
    transaction.notes = transaction_data.notes
    
    await db.flush()
    await db.refresh(transaction)
    return transaction

async def delete_transaction(db: AsyncSession, user_id: int, transaction_id: int) -> None:
    result = await db.execute(select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        )
    )
    
    transaction = result.scalar_one_or_none()
    
    if not transaction:
        raise NotFoundError("Transaction not found")
    
    await db.delete(transaction)
    await db.flush()    
    
async def create_budget(db: AsyncSession, user_id: int, budget_data: BudgetCreate) -> Budget:
    await _get_category_or_raise(db, budget_data.category_id, user_id)
    
    existing_budget = await db.execute(select(Budget).where(
            Budget.user_id == user_id,
            Budget.category_id == budget_data.category_id,
            Budget.month == budget_data.month
        )
    )
    
    budget = existing_budget.scalar_one_or_none()
    if budget:
        raise DuplicateError("Budget already exists")
    
    budget = Budget(
        user_id=user_id,
        category_id=budget_data.category_id,
        amount=budget_data.amount,
        month=budget_data.month
    )
    
    db.add(budget)
    await db.flush()
    await db.refresh(budget)
    return budget

async def _get_category_or_raise(db: AsyncSession, category_id: int, user_id: int) -> Category:
    result = await db.execute(
        select(Category).where(
            Category.id == category_id,
            or_(Category.user_id == user_id, Category.is_default.is_(True))
        )
    )
    category = result.scalar_one_or_none()
    if not category:
        raise NotFoundError("Category not found")
    return category
    
async def get_budgets(db: AsyncSession, user_id: int) -> list[Budget]:
    result = await db.execute(
        select(Budget).where(Budget.user_id == user_id)
    )
    return list(result.scalars().all())