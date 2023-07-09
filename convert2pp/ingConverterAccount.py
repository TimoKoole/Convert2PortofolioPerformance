import datetime
import os
import sys

import pandas as pd

import convert2pp.util as util


class IngConverterAccount:

    def dateparse(self, date):
        try:
            return datetime.datetime.strptime(date, '%d-%m-%Y')
        except:
            return ''

    def __init__(self, inputfile: str = None, data=None):
        self.note = 'convert2pp import at: ' + str(datetime.datetime.now())

        if data is None:
            self.inputdata = pd.read_csv(inputfile, parse_dates=[
                0], date_parser=self.dateparse, delimiter="\t", decimal=",",
                                         encoding='UTF-16LE')
        else:
            self.inputdata = data
        self.df = self.filter_input()
        # print(str(self.df.to_dict()).replace(" nan", " float('nan')"))
        self.outputdata = pd.DataFrame(
            index=self.df.index, columns=util.EXPORT_COLUMNS_ACCOUNT, data=None)

    def convert(self):
        self.outputdata['Date'] = self.df['Datum'].apply(util.convert_date)
        self.outputdata['Value'] = self.df['Bedrag']
        self.outputdata['Transaction Currency'] = 'EUR'
        self.outputdata['Note'] = self.note

        self.outputdata.loc[self.df['Omschrijving'].str.contains("Basisfee"), 'Type'] = 'Fees'
        self.outputdata.loc[self.df['Omschrijving'].str.contains("Kosten beleggen"), 'Type'] = 'Deposit'
        self.outputdata.loc[
            self.df['Omschrijving'].str.contains("Overschrijving beleggingsrekening"), 'Type'] = 'Deposit'

    def write_outputfile(self, outputfile: str):
        self.outputdata.to_csv(outputfile, decimal=".", sep=";")
        print("Wrote output to: " + outputfile)

    def filter_input(self):
        df = self.inputdata

        # exclude this selection
        try:
            df = df[~df["Omschrijving"].str.contains('koop')]
            df = df[~df["Omschrijving"].str.contains('Dividenden')]
        except KeyError as e:
            print("Failed to exclude buy orders")
            print(df)
            raise e

        return df


# https://mijn.ing.nl/investments/cash-transactions
if __name__ == '__main__':
    converter = IngConverterAccount(
        os.path.dirname(sys.argv[0]) + '/cash_transaction_overview_14086339-100-1-14086338_2023-06-01_2023-07-09.csv')
    converter.convert()
    filename = os.path.join(os.getcwd(), 'ing_account_converted.csv')
    converter.write_outputfile(filename)
