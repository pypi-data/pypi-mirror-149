from __future__ import annotations

import sys

import _csv

from ledger_importer.config import Config
from ledger_importer.transaction import Transaction


class TransactionsHandler:
    config: Config

    def __init__(self, config: Config) -> None:
        self.config = config

    def row_to_transaction(self, row: tuple) -> Transaction:
        return Transaction(
            date=self.config.parse_date(row),
            description=self.config.parse_description(row),
            amount=self.config.parse_amount(row),
            payee=self.config.parse_payee(row),
            account=self.config.parse_account(row),
        )

    def merge_transactions(self, transactions: list[Transaction]) -> list[Transaction]:
        """
        Take a list of transactions already sorted by date (oldest -> newest).
        Update the payees of the transactions when they seem to match.

        The matching is tried only on positive transactions, in this case
        it will look for older matching transactions.
        """
        merged_transactions: list[Transaction] = []

        for transaction in transactions:
            if transaction.amount > 0:
                for matching_transaction in transactions:
                    if matching_transaction is transaction:
                        # Nothing was found up to the current transaction
                        break

                    if self.config.transactions_match(transaction, matching_transaction):
                        transaction.payee = matching_transaction.account
                        merged_transactions.append(matching_transaction)
                        break

        return [transaction for transaction in transactions if transaction not in merged_transactions]

    def parse_transactions(self, csv_reader: _csv._reader) -> list[Transaction]:
        """
        Parse transactions from the csv reader and sort them chronologically.
        """
        transactions: list[Transaction] = []

        for _ in range(self.config.skip_lines):
            next(csv_reader)

        for row in csv_reader:
            transaction = self.row_to_transaction(tuple(row))
            transactions.append(transaction)

        return sorted(transactions, key=lambda transaction: transaction.date)

    def confirm_transactions(self, transactions: list[Transaction]) -> list[Transaction]:
        """
        Manually confirm the transactions using the cli.

        Returns only confirmed transactions.
        """
        confirmed_transactions: list[Transaction] = []

        for transaction in transactions:
            print(
                f"""
| {"Account".center(max(len(transaction.account), len("Account")))} | {"Date".center(10)} | {"Amount".center(max(len(self.config.format_amount(transaction.amount)), len("Amount")))} | {"Description".center(max(len(transaction.description), len("Description")))} |
| {transaction.account} | {transaction.date.strftime("%Y/%m/%d")} | {self.config.format_amount(transaction.amount)} | {transaction.description} |
    """,
                file=sys.stderr,
            )

            if transaction.amount > 0:
                print(
                    f"""Which account provided this income? ([{transaction.payee}]/[q]uit/[s]kip) """,
                    file=sys.stderr,
                )
            else:
                print(
                    f"""To which account did this money go? ([{transaction.payee}]/[q]uit/[s]kip) """,
                    file=sys.stderr,
                )

            answer = input()
            if answer == "q":
                break
            elif answer == "s":
                continue

            if answer:
                transaction = Transaction(
                    date=transaction.date,
                    description=transaction.description,
                    amount=transaction.amount,
                    payee=answer,
                    account=transaction.account,
                )
            confirmed_transactions.append(transaction)

        return confirmed_transactions
