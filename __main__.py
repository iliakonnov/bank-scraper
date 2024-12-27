import dataclasses
import itertools
import json
import sys
import csv

import haralyzer

import banks
from models import CSVRow

accounts = {
    'tinkoff-5696181790': 'T-Debit',
    'tinkoff-0763313608': 'T-Credit',
    'tinkoff-5727532300': False,  # Junior
    'tinkoff-8246809001': 'T-Account',
    'tinkoff-6109852795': 'T-Mobile',

    'ardshin-2470087002440000': 'A-AMD',
    'ardshin-2470087002440010': 'A-USD',
    'ardshin-2470087002440020': False,  # clone of A-VISA
    'ardshin-4454300003735591': 'A-VISA',

    'yabank-PAY_CARD': 'Y-Card',
    'yaplus': 'Y-Plus',

}

if __name__ == "__main__":
    entries = []
    for fname in sys.argv[1:]:
        with open(fname, 'r') as f:
            data = json.load(f)
        entries += [entry for page in haralyzer.HarParser(data).pages for entry in page.entries]

    transactions = itertools.chain(
        banks.tinkoff.extract(entries),
        banks.ardshin.extract(entries),
        banks.yabank.extract(entries),
        banks.yaplus.extract(entries),
    )
    transactions = sorted(
        {txn.external_id: txn for txn in transactions}.values(),
        key=lambda txn: txn.date
    )

    fields = [i.name for i in dataclasses.fields(CSVRow)]
    writer = csv.DictWriter(sys.stderr, fields)
    writer.writeheader()
    writer.writerows(
        dataclasses.asdict(CSVRow(
            date=txn.date.date(),
            amount=txn.amount.value * (1 if txn.type == 'deposit' else -1),
            name=txn.description,
            currency=txn.amount.currency,
            category='',
            tags='',
            account=accounts.get(txn.account_id, txn.account_id),
            notes=txn.notes,
        ))
        for txn in transactions
        if accounts.get(txn.account_id) is not False
    )
