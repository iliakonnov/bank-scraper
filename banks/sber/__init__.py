import json
from datetime import datetime, timezone
from decimal import Decimal
from typing import Iterable
from zoneinfo import ZoneInfo

import ftfy
from ftfy import fix_encoding
from haralyzer import HarEntry

from banks.sber.models import Model

from models import Transaction, Amount

"""
1. Transfer between accounts
    from:
    to:
    amount in negative

2. Income
    to:
    amount in positive

3. Payment
    from:
    amount is negative
"""


def extract(entries: list[HarEntry]) -> Iterable[Transaction]:
    for entry in entries:
        if entry.request.method != 'POST':
            continue
        if not entry.request.url.startswith('https://web-node7.online.sberbank.ru/uoh-bh/v1/operations/list'):
            continue
        response: Model = json.loads(entry.response.text)
        for op in response['body']['operations']:
            if 'operationAmount' not in op:
                continue
            amount = Decimal(op['operationAmount']['amount'])
            if amount == 0:
                continue

            if acc_id := op.get('fromResource', {}).get('id'):
                yield Transaction(
                    type='withdrawal' if amount < 0 else 'deposit',
                    date=datetime.strptime(op['date'], '%d.%m.%YT%H:%M:%S').astimezone(ZoneInfo("Europe/Moscow")),
                    description=op['correspondent'],
                    amount=Amount(
                        value=abs(amount).quantize(Decimal("0.0001")),
                        currency=op['operationAmount']['currencyCode']
                    ),
                    external_id='sber-from-' + op['uohId'],
                    account_id=f'sber-{acc_id}',
                    notes=op['description'],
                )
            if acc_id := op.get('toResource', {}).get('id'):
                assert amount > 0 or 'fromResource' in op
                yield Transaction(
                    type='deposit',
                    date=datetime.strptime(op['date'], '%d.%m.%YT%H:%M:%S').astimezone(ZoneInfo("Europe/Moscow")),
                    description=op['correspondent'],
                    amount=Amount(
                        value=abs(amount).quantize(Decimal("0.0001")),
                        currency=op['operationAmount']['currencyCode']
                    ),
                    external_id='sber-to-' + op['uohId'],
                    account_id=f'sber-{acc_id}',
                    notes=op['description'],
                )
