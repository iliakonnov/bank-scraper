import json
from datetime import datetime, timezone
from decimal import Decimal
from typing import Iterable
from zoneinfo import ZoneInfo

from haralyzer import HarEntry

from banks.credo.models import Model

from models import Transaction, Amount


def extract(entries: list[HarEntry]) -> Iterable[Transaction]:
    for entry in entries:
        if entry.request.method != 'POST':
            continue
        if not entry.request.url.startswith('https://mycredo.ge:8443/graphql'):
            continue
        request = json.loads(entry.request.text)
        if request['operationName'] != 'transactionPagingList':
            continue
        response: Model = json.loads(entry.response.text)
        for item in response['data']['transactionPagingList']['itemList']:
            assert (item['debit'] or item['credit']) and not (item['debit'] and item['credit'])
            yield Transaction(
                type='withdrawal' if item['debit'] else 'deposit',
                date=datetime.fromisoformat(item['operationDateTime']).astimezone(ZoneInfo('Asia/Tbilisi')),
                description=item['description'],
                amount=Amount(
                    value=Decimal(item['debit'] or item['credit']).quantize(Decimal("0.0001")),
                    currency=item['currency']
                ),
                external_id='credo-' + item['transactionId'],
                account_id=f'credo-{item["accountNumber"]}-{item["currency"]}',
            )
