import typer

app = typer.Typer()

SAMPLE_CONFIG = """#!/usr/bin/env python
from __future__ import annotations

import datetime
import re
from decimal import Decimal

from ledger_importer import Config, runner, Posting, Amount

# Custom ledger importer configuration
class LedgerImporterConfig(Config):
    # Define the number of lines that needs to be skipped at the beginning of the file.
    # This is usefull if the csv has a line with the column names for example.
    skip_lines: int = 1

    # Define the csv delimiter
    csv_delimiter: str = ","

    # The argument `fields` given in all parse_* methods contains a whole csv row in a tuple
    # Each element of the tuple is a string representation of the column

    def parse_date(self, fields: tuple) -> datetime.datetime:
        return datetime.datetime.strptime(fields[0], "%m-%d-%Y")

    def parse_payee(self, fields: tuple) -> str:
        return fields[2]

    def parse_postings(self, fields: tuple) -> list[Posting]:
        amount = Amount(quantity=Decimal(re.sub("[€ ]", "", fields[3]).replace(",", ".")), commodity="€")
        if amount > 0:
            account = "Income"
        else:
            account = "Expenses"

        posting = Posting(account="Assets:Checking", amount=amount)

        # A Transaction should be at least 2 postings that have reversed amounts
        return [posting, Posting(account=account, amount=amount.reverse())]


# The next lines are required to run ledger_importer
# when the config file is executed.
if __name__ == "__main__":
    runner(LedgerImporterConfig())
"""


@app.command("init")
def init():
    """
    Bootstrap a config file that can later be customized.
    """
    print(SAMPLE_CONFIG)


if __name__ == "__main__":
    app()
