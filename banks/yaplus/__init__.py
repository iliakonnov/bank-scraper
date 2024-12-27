import json
from datetime import datetime
from decimal import Decimal
from typing import Iterable

from haralyzer import HarEntry

from banks.yaplus.models import Model

from models import Transaction, Amount


def extract(entries: list[HarEntry]) -> Iterable[Transaction]:
    for entry in entries:
        if entry.request.method != 'POST':
            continue
        if not entry.request.url.startswith('https://id.yandex.ru/front-api/graphql'):
            continue
        request = json.loads(entry.request.text)[0]
        if request['operationName'] != 'PaymentsList':
            continue
        response: Model = json.loads(entry.response.text)
        for order in response[0]['data']['paymentsList']['orders']:
            for payment in [order['rootPayment'],
                            *order['linkedTransactions']]:  # type: models.RootPayment | models.LinkedTransaction
                if payment['status'] != 'Paid':
                    continue
                if payment['paymentMethod'] not in ('yandex_account_withdraw', 'yandex_account_topup'):
                    continue
                yield Transaction(
                    type='withdrawal' if payment['paymentMethod'] == 'yandex_account_withdraw' else 'deposit',
                    date=datetime.fromisoformat(order['created']),
                    description=order['service'],
                    amount=Amount(
                        value=Decimal(payment['total']).quantize(Decimal("0.0001")),
                        currency='RUB',
                    ),
                    external_id=order['id'],
                    account_id='yaplus',
                )
