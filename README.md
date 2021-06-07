# Convert to portfolio performance

## Degiro
### Account.csv
DegiroType: Rekening
portofolio performance type: Account
import twice, one for usd account one for EUR account

### Transactions.csv
As of now Transaction import by PDF actually works fine out of the box

## ING
Transactions --> Wijzigingen in portefeuille
Account --> Af en bij

## Setup and install
* create distribution by `python setup.py sdist`
* install package by `pip install dist/convert2pp-0.0.1.tar.gz`