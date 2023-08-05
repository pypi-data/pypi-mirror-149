from __future__ import annotations

import datetime
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Transaction:
    """
    Representation of a Transaction.
    """

    date: datetime.datetime
    description: str
    amount: Decimal
    payee: str
    account: str

    def to_ledger(self, config):
        return f"""{self.date.strftime("%Y/%m/%d")}    {self.description}
    {self.account}    {config.format_amount(self.amount)}
    {self.payee}
"""
