from dataclasses import dataclass, field
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
    category: str = ''
    tags: list['str'] = field(default_factory=list)


@dataclass(kw_only=True)
class CSVRow:
    id: str
    date: datetime | date
    amount: Decimal
    name: str
    currency: str
    category: str
    tags: str
    account: str
    notes: str
