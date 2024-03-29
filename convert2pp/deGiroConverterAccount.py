import datetime
import logging
import os
import sys

import pandas as pd
from currency_converter import CurrencyConverter

import convert2pp.util
import convert2pp.util as util

c = CurrencyConverter(fallback_on_missing_rate=True, fallback_on_wrong_date=True)
convert_isin_usd_to_euro = ['IE00B3RBWM25', 'IE00B0M62Q58', 'IE0031442068', 'IE00BZ163M45']


def convert_currency(isin: str, value: str, date):
    if isin in convert_isin_usd_to_euro:
        try:
            converted = c.convert(value, 'USD', 'EUR', date=date)
            return round(converted, 2)
        except Exception as e:
            logging.exception("message")
            print(isin + str(value) + str(date))
            return value
    return value


class DeGiroConverterAccount:

    def dateparse(self, date):
        try:
            return datetime.datetime.strptime(date, '%d-%m-%Y')
        except:
            return ''

    def __init__(self, inputfile: str = None, data=None):
        self.note = 'convert2pp import at: ' + str(datetime.datetime.now())

        if data is None:
            self.inputdata = pd.read_csv(inputfile, parse_dates=[
                0], date_parser=self.dateparse, decimal=",")
        else:
            self.inputdata = data
        self.df = self.filter_input()
        # print(str(self.df.to_dict()).replace(" nan", " float('nan')"))
        self.outputdata = pd.DataFrame(
            index=self.df.index, columns=util.EXPORT_COLUMNS_ACCOUNT, data=None)

    def convert(self):
        self.outputdata['Date'] = self.df['Datum'].apply(convert2pp.util.convert_date)
        self.outputdata['ISIN'] = self.df['ISIN']
        self.df['Value'] = self.df.iloc[:, 8].astype(float)
        self.outputdata['Transaction Currency'] = self.df['Mutatie']
        self.outputdata['Note'] = self.note
        self.outputdata.loc[self.df['Omschrijving'].str.contains("Dividendbelasting"), 'Type'] = 'Taxes'
        self.outputdata.loc[self.df['Omschrijving'].str.contains("iDEAL"), 'Type'] = 'Deposit'
        # DeGiro has a weird issue in that some EUR funds pay out dividend in USD
        # This completely messes up the imports since pp does not expect that
        # Therefore we manually convert those funds to EUR. This will probably be off by some margin,
        # but I can live with that
        self.outputdata.loc[self.outputdata['ISIN'].isin(convert_isin_usd_to_euro), 'Transaction Currency'] = 'EUR'
        self.outputdata['Value'] = self.df.apply(lambda row: convert_currency(row['ISIN'], row['Value'], row['Datum']),
                                                 axis=1)

    def write_outputfile(self, outputfile: str):
        self.outputdata.to_csv(outputfile, decimal=".", sep=";")
        print("Wrote output to: " + outputfile)

    def filter_input(self):
        df = self.inputdata

        # exclude this selection, these transactions are weird and are braking things.
        df = df[~df["Omschrijving"].str.contains('geldmarktfonds')]

        # This is the final selection
        df = df[(df['Omschrijving'].str.contains("Dividend")) | (
            df['Omschrijving'].str.contains('iDEAL Deposit'))]

        return df


if __name__ == '__main__':
    converter = DeGiroConverterAccount(os.path.dirname(sys.argv[0]) + '\\Account.csv')
    converter.convert()
    filename = os.path.join(os.getcwd(), "degiro_account_converted.csv")
    converter.write_outputfile(filename)
