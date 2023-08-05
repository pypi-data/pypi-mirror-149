from __future__ import annotations

import csv
import pathlib
import re
import readline
from typing import Optional

import typer

from ledger_importer.config import Config
from ledger_importer.transaction import Amount
from ledger_importer.transaction import Posting
from ledger_importer.transaction import Transaction
from ledger_importer.transactions_handler import TransactionsHandler

__all__ = ("Config", "runner", "Amount", "Posting", "Transaction")


ACCOUNT_LINE = r"^account ([A-z_ :]*[A-z])( +;?.*)?"


def parse_accounts(data: str) -> list[str]:
    accounts: list[str] = []

    for line in data.split("\n"):
        m = re.match(ACCOUNT_LINE, line)
        if not m:
            continue
        accounts.append(m.groups()[0])

    return accounts


class AccountCompleter:
    def __init__(self, accounts: list[str]) -> None:
        self.accounts = accounts

    def complete(self, text: str, state: int) -> str | None:
        # on first trigger, build possible matches
        if state == 0:
            if not text:
                self.matches = self.accounts[:]
            else:
                self.matches = [s for s in self.accounts if s and s.startswith(text)]

        try:
            return self.matches[state]
        except IndexError:
            pass

        return None


def main_wrapper(config: Config):
    def main(
        csv_path: pathlib.Path = typer.Argument(..., help="Path to the bank statement to import."),
        journal_path: Optional[pathlib.Path] = typer.Option(
            None, help="Path a ledger journal to write & learn accounts from."
        ),
        quiet: bool = typer.Option(False, help="Don't ask questions and guess all the accounts automatically."),
    ):
        """
        Import a bank statement.
        """
        # Get accounts list
        accounts: list[str] = []
        if journal_path:
            with journal_path.open() as journal_file:
                accounts = parse_accounts(journal_file.read())

        # Setup account completion
        completer = AccountCompleter(accounts)
        readline.set_completer(completer.complete)
        readline.parse_and_bind("tab: complete")
        readline.set_completer_delims(" \t\n;")

        # Parse transactions, merge them and confirm them
        handler = TransactionsHandler(config)

        with csv_path.open() as csv_file:
            transactions = handler.merge_transactions(
                handler.parse_transactions(
                    csv.reader(csv_file, delimiter=config.csv_delimiter),
                ),
            )
            if not quiet:
                transactions = handler.confirm_transactions(transactions)

        for transaction in transactions:
            print(transaction.to_ledger())

    return main


def runner(config: Config):
    typer.run(main_wrapper(config))
