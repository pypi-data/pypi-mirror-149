from __future__ import annotations

import sys

import _csv

from ledger_importer.config import Config
from ledger_importer.transaction import Amount
from ledger_importer.transaction import Posting
from ledger_importer.transaction import Transaction


class TransactionsHandler:
    config: Config

    def __init__(self, config: Config) -> None:
        self.config = config

    def row_to_transaction(self, row: tuple) -> Transaction:
        return Transaction(
            date=self.config.parse_date(row),
            payee=self.config.parse_payee(row),
            postings=self.config.parse_postings(row),
        )

    def merge_transactions(self, transactions: list[Transaction]) -> list[Transaction]:
        """
        Take a list of transactions already sorted by date (oldest -> newest).
        Update the target_accounts of the transactions when they seem to match.

        The matching is tried only on positive transactions, in this case
        it will look for older matching transactions.
        """
        merged_transactions: list[Transaction] = []

        for transaction in transactions:
            if transaction.postings[0].amount > 0:
                for matching_transaction in transactions:
                    if any(matching_transaction is t for t in merged_transactions):
                        # Transaction can be merged only once
                        continue

                    if matching_transaction.date > transaction.date:
                        # Nothing was found up to the current transaction
                        break

                    if self.config.transactions_match(transaction, matching_transaction):
                        transaction.postings[1].account = matching_transaction.postings[0].account
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
| {"Account".center(max(len(transaction.postings[0].account), len("Account")))} | {"Date".center(10)} | {"Amount".center(max(len(str(transaction.postings[0].amount)), len("Amount")))} | {"Payee".center(max(len(transaction.payee), len("Payee")))} |
| {transaction.postings[0].account} | {transaction.date.strftime("%Y/%m/%d")} | {transaction.postings[0].amount} | {transaction.payee} |
    """,
                file=sys.stderr,
            )

            if transaction.postings[0].amount.quantity > 0:
                print(
                    f"""Which account provided this income? ([{transaction.postings[1].account}]/[q]uit/[s]kip) """,
                    file=sys.stderr,
                )
            else:
                print(
                    f"""To which account did this money go? ([{transaction.postings[1].account}]/[q]uit/[s]kip) """,
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
                    payee=transaction.payee,
                    postings=[
                        transaction.postings[0],
                        Posting(
                            account=answer,
                            amount=Amount(
                                quantity=transaction.postings[1].amount.quantity,
                                commodity=transaction.postings[1].amount.commodity,
                            ),
                        ),
                    ],
                )
            confirmed_transactions.append(transaction)

        return confirmed_transactions
