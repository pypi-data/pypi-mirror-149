from __future__ import annotations

import datetime
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Amount:
    quantity: Decimal
    commodity: str

    def __str__(self) -> str:
        return f"{self.quantity} {self.commodity}"

    def reverse(self) -> Amount:
        return Amount(quantity=-self.quantity, commodity=self.commodity)

    def __gt__(self, val) -> bool:
        return self.quantity > val


@dataclass
class Posting:
    account: str
    amount: Amount


@dataclass
class Transaction:
    """
    Representation of a Transaction.
    """

    date: datetime.datetime
    payee: str
    postings: list[Posting]

    def to_ledger(self):
        return (
            f"{self.date.strftime('%Y/%m/%d')}    {self.payee}\n"
            + "\n".join([f"    {posting.account}    {posting.amount}" for posting in self.postings])
            + "\n"
        )
