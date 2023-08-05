from __future__ import annotations

import datetime
from abc import ABC
from abc import abstractmethod
from decimal import Decimal

from ledger_importer.transaction import Transaction


class Config(ABC):
    skip_lines: int = 1
    csv_delimiter: str = ","
    default_account: str = "Assets:Checking"

    @abstractmethod
    def parse_date(self, fields: tuple) -> datetime.datetime:
        pass

    @abstractmethod
    def parse_description(self, fields: tuple) -> str:
        pass

    @abstractmethod
    def parse_amount(self, fields: tuple) -> Decimal:
        pass

    @abstractmethod
    def format_amount(self, amount: Decimal) -> str:
        pass

    @abstractmethod
    def parse_payee(self, fields: tuple) -> str:
        pass

    @abstractmethod
    def parse_account(self, fields: tuple) -> str:
        pass

    def transactions_match(self, transaction1: Transaction, transaction2: Transaction) -> bool:
        """
        Matching transactions will get merged in a single transaction.

        When they are merged, the payee of transaction1 will be updated to the account of transaction2. This overrides the parse_payee return value.

        Default behavior is to merge transactions with opposite amounts and different accounts.
        """
        return transaction1.amount == -transaction2.amount and transaction1.account != transaction2.account
