import json
from datetime import datetime
from decimal import Decimal
from typing import Iterable
from zoneinfo import ZoneInfo

from iso4217 import iso4217
from haralyzer import HarEntry

from banks.ardshin.models import Model

from models import Transaction, Amount


# https://ibanking.ardshinbank.am/nibanking/accounts


def extract(entries: list[HarEntry]) -> Iterable[Transaction]:
    for entry in entries:
        if entry.request.method != 'POST':
            continue
        if not entry.request.url.startswith('https://ibanking.ardshinbank.am/nibanking/bc_ashb_api/get_ASHB.php'):
            continue
        response: Model = json.loads(entry.response.text)
        if response.get('@attributes').get('operation') != 'getAccountTransactions':
            continue
        params = json.loads(entry.request['postData']['params'][0]['value'])['getAccountTransactionsParameters']
        operations = response['getAccountTransactions']['Operation']
        if not isinstance(operations, list):
            operations = [operations]
        account_id = 'ardshin-' + params['objectID']
        for op in operations:
            yield Transaction(
                type={'1': 'withdrawal', '2': 'deposit'}[op['operation']],
                date=(datetime
                      .strptime(f"{op['valueDate']} {op['time']}", "%d.%m.%Y %H:%M")
                      .astimezone(ZoneInfo("Asia/Yerevan"))),
                description=op['details'].split('\\')[-1].replace('\n', ' '),
                account_id=account_id,
                amount=Amount(
                    value=Decimal(op['amount']),
                    currency=iso4217[op['currency']]
                ),
                external_id=f"{account_id} / {op['refnum']}",
                notes=op['description']['translation'][0]['@attributes']['value'],
            )
