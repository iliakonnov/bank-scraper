import json
from datetime import datetime, timezone
from decimal import Decimal
from typing import Iterable
from zoneinfo import ZoneInfo

from haralyzer import HarEntry

from banks.vtb.models import Model

from models import Transaction, Amount


def extract(entries: list[HarEntry]) -> Iterable[Transaction]:
    for entry in entries:
        if entry.request.method != 'GET':
            continue
        if not entry.request.url.startswith('https://online.vtb.ru/msa/api-gw/private/history-hub/history-hub-homer/v1/history/byUser'):
            continue
        response: Model = json.loads(entry.response.text)
        for op in response['operations']:
            yield Transaction(
                type='withdrawal' if op['debet'] else 'deposit',
                date=datetime.fromisoformat(op['operationDate']).astimezone(ZoneInfo("Europe/Moscow")),
                description=op['operationName'],
                amount=Amount(
                    value=Decimal(op['operationAmount']['sum']).quantize(Decimal("0.0001")),
                    currency=op['operationAmount']['currency']
                ),
                external_id=op['operationId'],
                account_id=f'vtb-{op["accountProductId"]}',
                category=op.get('parentCategory', {}).get('name') or '',
            )
