from __future__ import annotations

import datetime
from abc import ABC
from abc import abstractmethod

from ledger_importer.transaction import Posting
from ledger_importer.transaction import Transaction


class Config(ABC):
    skip_lines: int = 1
    csv_delimiter: str = ","

    @abstractmethod
    def parse_date(self, fields: tuple) -> datetime.datetime:
        pass

    @abstractmethod
    def parse_payee(self, fields: tuple) -> str:
        pass

    @abstractmethod
    def parse_postings(self, fields: tuple) -> list[Posting]:
        pass

    def transactions_match(self, transaction1: Transaction, transaction2: Transaction) -> bool:
        """
        Matching transactions will get merged in a single transaction.

        When they are merged, the target_account of transaction1 will be updated to the account of transaction2. This overrides the parse_target_account return value.

        Default behavior is to merge transactions with opposite amounts and different accounts.
        """
        return (
            transaction1.postings[0].amount == transaction2.postings[0].amount.reverse()
            and transaction1.postings[0].account != transaction2.postings[0].account
        )
