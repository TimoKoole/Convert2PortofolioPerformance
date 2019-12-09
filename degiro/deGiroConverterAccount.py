import sys
import os
import pandas as pd
import logging

import degiro.util
import datetime
from currency_converter import CurrencyConverter

c = CurrencyConverter(fallback_on_missing_rate=True, fallback_on_wrong_date=True)
convert_isin=['IE00B3RBWM25', 'IE00B0M62Q58', 'IE0031442068', 'IE00BZ163M45']

def convert_currency(isin, value, date):
    if isin in convert_isin:
        try:
            converted = c.convert(float(value.replace(',','.')) , 'USD', 'EUR', date=date)
            return ('%.2f' % converted).replace('.',',')
        except Exception as e:
            logging.exception("message")
            print(isin + str(value) + str(date))
            return value
    return value


class DeGiroConverterAccount:
    EXPORT_COLUMNS = ["Date", "ISIN", "Value",
                      "shares", "Fees", 'Transaction Currency']

    def dateparse(self, date):
        try:
            return pd.datetime.strptime(date, '%d-%m-%Y')
        except:
            return ''


    def __init__(self, inputfile):
        self.note = 'Timo import at: ' + str(datetime.datetime.now())
        self.inputdata = pd.read_csv(inputfile, parse_dates=[
                                     0], date_parser=self.dateparse)
        self.df = self.filter_input()
        self.outputdata = pd.DataFrame(
            index=self.df.index, columns=self.EXPORT_COLUMNS, data=None)


    def convert(self):
        self.outputdata['Date'] = self.df['Datum'].apply(degiro.util.convert_date)
        self.outputdata['ISIN'] = self.df['ISIN']
        self.df['Value'] = self.df.iloc[:, 8]
        self.outputdata['Transaction Currency'] = self.df['Mutatie']
        self.outputdata['Note'] = self.note

        # custom overwrite
        self.outputdata['Transaction Currency'] [self.outputdata['ISIN'].isin(convert_isin)]  = 'EUR'
        # gapminder[gapminder['year'] == 2002]
        self.outputdata['Value'] = self.df.apply(lambda row: convert_currency(row['ISIN'], row['Value'], row['Datum']), axis=1)

    def write_outputfile(self, outputfolder, outputfile):
        os.makedirs(outputfolder, exist_ok=True)
        self.outputdata.to_csv(os.path.join(
            outputfolder, outputfile), decimal=",", sep=",")

    def filter_input(self):
        df = self.inputdata
        df = df[(df['Omschrijving'] == "Dividend") | (
            df['Omschrijving'] == "iDEAL storting")]
        df = df[~df["Omschrijving"].str.contains('geldmarktfonds')]
        return df


if __name__ == '__main__':
    converter = DeGiroConverterAccount(
        os.path.dirname(sys.argv[0]) + '\\Account.csv')
    converter.convert()
    converter.write_outputfile(os.path.dirname(
        sys.argv[0]), 'degiro_account_converted.csv')
