# Convert DeGiro to portfolio performance

## Account.csv
DegiroType: Rekening
portofolio performance type: Account
import twice, one for usd account one for EUR account

## Transactions.csv
As of now Transaction import by PDF actually works fine out of the box


## Run unit tests
`python -m unittest discover -v`

## Setup and install
* create distribution by `python setup.py sdist`
* install package by `pip install dist/degiro2pp-0.0.1.tar.gz` 

## How to run
* `python -m ING2YNAB --input transactions.csv --output ING.csv`