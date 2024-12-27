import json
from datetime import datetime
from decimal import Decimal
from typing import Iterable

from haralyzer import HarEntry

from banks.tinkoff.models import Model

from models import Transaction, Amount


def extract(entries: list[HarEntry]) -> Iterable[Transaction]:
    for entry in entries:
        if entry.request.method != 'GET':
            continue
        if not entry.request.url.startswith('https://www.tbank.ru/api/common/v1/operations'):
            continue
        response: Model = json.loads(entry.response.text)
        for data in response['payload']:
            yield Transaction(
                type='withdrawal' if data['type'] == 'Debit' else 'deposit',
                date=datetime.fromtimestamp(data['operationTime']['milliseconds'] / 1000),
                description=data['description'],
                amount=Amount(
                    value=Decimal(data['accountAmount']['value']).quantize(Decimal("0.0001")),
                    currency=data['accountAmount']['currency']['name']
                ),
                foreign_amount=Amount(
                    value=Decimal(data['amount']['value']).quantize(Decimal("0.0001")),
                    currency=data['amount']['currency']['name']
                ),
                external_id=data['id'],
                account_id=f'tinkoff-{data["account"]}',
            )
