# Convert to portfolio performance

## Degiro

### Account.csv

* DegiroType: Rekeningoverzicht <https://trader.degiro.nl/trader/#/account-overview>
* portofolio performance type: Account
* import twice, one for usd account one for EUR account

### Transactions.csv

As of now Transaction import by PDF actually works fine out of the box

## ING

* Transactions --> <https://mijn.ing.nl/investments/portfolio-transactions>
* Account --> <https://mijn.ing.nl/investments/cash-transactions>

## Setup and install

* create distribution by `python setup.py sdist`
* install package by `pip install dist/convert2pp-0.0.1.tar.gz`
