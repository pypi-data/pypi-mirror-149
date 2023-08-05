# ledger_importer [![CircleCI](https://circleci.com/gh/volnt/ledger_importer.svg?style=shield&circle-token=afb73aed03518c8658de39f5d61ec3bfdf50d57c)](https://app.circleci.com/settings/project/github/volnt/ledger_importer)

ledger_importer is a csv-to-[ledger](https://www.ledger-cli.org/3.0/doc/ledger3.html) importer that can be configured in Python.

The key features are:

* **Customization**: Designed to fit your specific needs perfectly.
* **Auto-completion**: The confirmation step is auto-completed.
* **Integration**: Easy to integrate with your pipeline.

## Installation

```sh
$ pip install ledger-importer
```

## Configure

ledger_importer works by using the configuration file as the entrypoint. The `ledger_importer.runner` function is the function that should be called when you want to run the program.

The `runner` function takes a Config as the first argument.

A Config instance can be created by creating a new class that inherits `ledger_importer.runner`. This new class must implement the following methods:

* `parse_date(self, fields: tuple) -> datetime.datetime`
* `parse_description(self, fields: tuple) -> str`
* `parse_amount(self, fields: tuple) -> Decimal`
* `format_amount(self, amount: Decimal) -> str`
* `parse_payee(self, fields: tuple) -> str`
* `parse_account(self, fields: tuple) -> str`

The argument `fields: tuple` will be the csv row, with each column as an element of the tuple.


Example configuration file:

```py
# Name: my_importer.py

from __future__ import annotations

import datetime
import re
from decimal import Decimal

from ledger_importer import Config, runner

EXPENSES_MATCHER = {
    "Expenses:Groceries": [
        "costco",
    ],
    "Expenses:Subscriptions": [
        "netflix",
        "spotify",
    ],
    "Expenses:Shopping": [
        "amazon",
        "paypal",
    ],
}


class LedgerImporterConfig(Config):
    """
    Our custom importer configuration.

    All methods defined here must be defined to parse the csv.
    """
    skip_lines: int = 1

    def parse_date(self, fields: tuple) -> datetime.datetime:
        return datetime.datetime.strptime(fields[0], "%m-%d-%Y")

    def parse_description(self, fields: tuple) -> str:
        return fields[2]

    def parse_amount(self, fields: tuple) -> Decimal:
        return Decimal(re.sub("[$,]", "", fields[3))

    def format_amount(self, amount: Decimal) -> str:
        return f"${amount}"

    def parse_payee(self, fields: tuple) -> str:
        if self.parse_amount(fields) > 0:
            return "Income"

        # Match the transaction with a payee based on regexp defined
        # in EXPENSES_MATCHER.
        for payee, exps in EXPENSES_MATCHER.items():
            for exp in exps:
                if re.match(rf".*{exp}.*", fields[2]):
                    return payee

        # Default to Expenses
        return "Expenses"

    def parse_account(self, fields: tuple) -> str:
        return "Assets:Checking"


# The next lines are required to run ledger_importer
# when the config file is executed.
if __name__ == "__main__":
    runner(LedgerImporterConfig())
```

## Run

To run leger_importer, run the configuration module:

```sh
$ python my_importer.py bank-statement.csv --journal-path journal.ledger

|        Account         |    Date    |  Amount  |     Description     |
| Assets:Account:Florent | 2021/07/29 | 1234.56€ | VIR LOLE FOOB A.R.L |

Which account provided this income? ([Income:Salary]/[q]uit/[s]kip)


|        Account         |    Date    |  Amount |         Description          |
| Assets:Account:Florent | 2021/08/02 | -11.77€ | CARD  27/07/21 SWILE XX*XXXX |

To which account did this money go? ([Expenses:Restaurant]/[q]uit/[s]kip)


|        Account         |    Date    |   Amount  |               Description               |
| Assets:Account:Florent | 2021/08/03 |  -784.00€ | VIR Save some € Mr.      Florent        |

To which account did this money go? ([Expenses]/[q]uit/[s]kip)
Assets:Savings


|        Account         |    Date    |  Amount |          Description          |
| Assets:Account:Florent | 2021/08/03 | -58.63€ | CARD  08/03/21 PAYPAL XX*XXXX |

To which account did this money go? ([Expenses:Shopping]/[q]uit/[s]kip)
q
```

## Usage

```sh
$ python my_importer.py --help
Usage: my_importer.py [OPTIONS] CSV_PATH

Arguments:
  CSV_PATH  Path to the bank statement to import.  [required]

Options:
  --journal-path PATH             Path a ledger journal to write & learn
                                  accounts from.
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```
