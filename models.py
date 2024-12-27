from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from typing import Literal


@dataclass
class Amount:
    value: Decimal
    currency: str


@dataclass(kw_only=True)
class Transaction:
    type: Literal['withdrawal', 'deposit']
    date: datetime
    amount: Amount
    description: str
    account_id: str
    external_id: str
    notes: str = ''
    foreign_amount: Amount | None = None


@dataclass(kw_only=True)
class CSVRow:
    date: datetime | date
    amount: Decimal
    name: str
    currency: str
    category: str
    tags: str
    account: str
    notes: str
