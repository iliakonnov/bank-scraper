import dataclasses
import itertools
import json
import sys
import csv

import haralyzer
import ftfy
from pyjson5 import pyjson5

import banks
from models import CSVRow

if __name__ == "__main__":
    with open('accounts.json5', 'r') as f:
        accounts = pyjson5.load(f)

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
        banks.sber.extract(entries),
        banks.vtb.extract(entries),
        banks.credo.extract(entries),
    )
    transactions = sorted(
        {txn.external_id: txn for txn in transactions}.values(),
        key=lambda txn: txn.date
    )

    fields = [i.name for i in dataclasses.fields(CSVRow)]
    writer = csv.DictWriter(sys.stdout, fields)
    writer.writeheader()
    writer.writerows(
        dataclasses.asdict(CSVRow(
            id=txn.external_id,
            date=txn.date.replace(microsecond=0),
            amount=txn.amount.value * (1 if txn.type == 'deposit' else -1),
            name=ftfy.fix_encoding(txn.description),
            currency=txn.amount.currency,
            category=ftfy.fix_encoding(txn.category),
            tags=ftfy.fix_encoding('|'.join(txn.tags)),
            account=accounts.get(txn.account_id, txn.account_id),
            notes=ftfy.fix_encoding(txn.notes),
        ))
        for txn in transactions
        if accounts.get(txn.account_id) is not False
    )
