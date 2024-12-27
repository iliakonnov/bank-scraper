import json
from datetime import datetime
from decimal import Decimal
from typing import Iterable

from haralyzer import HarEntry

from banks.yabank.models import Model

from models import Transaction, Amount


def extract(entries: list[HarEntry]) -> Iterable[Transaction]:
    for entry in entries:
        if entry.request.method != 'POST':
            continue
        if not entry.request.url.startswith('https://bank.yandex.ru/graphql'):
            continue
        request = json.loads(entry.request.text)
        if request['operationName'] != 'GetTransactionFeedView':
            continue
        if request['variables'].get('filterType') != 'PAY_CARD':
            continue
        response: Model = json.loads(entry.response.text)
        for item in response['data']['getTransactionsFeedView']['items']:
            if item['statusCode'] != 'CLEAR':
                continue
            yield Transaction(
                type='withdrawal' if item['directionV2'] == 'DEBIT' else 'deposit',
                date=datetime.fromisoformat(item['date']),
                description=item['title']['plain'],
                amount=Amount(
                    value=Decimal(item['amount']['money']['amount']).quantize(Decimal("0.0001")),
                    currency=item['amount']['money']['currency'],
                ),
                external_id=item['id'],
                account_id=f'yabank-PAY_CARD',
            )