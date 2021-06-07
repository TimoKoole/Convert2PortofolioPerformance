import datetime
import logging
import os
import sys
import convert2pp.util as util

import pandas as pd


import convert2pp.util



class IngConverterAccount:

    def dateparse(self, date):
        try:
            return datetime.datetime.strptime(date, '%Y-%m-%d')
        except:
            return ''

    def __init__(self, inputfile: str = None, data=None):
        self.note = 'degiro2pp import at: ' + str(datetime.datetime.now())

        if data is None:
            self.inputdata = pd.read_csv(inputfile, parse_dates=[
                0], date_parser=self.dateparse, delimiter=";",)
        else:
            self.inputdata = data
        self.df = self.filter_input()
        # print(str(self.df.to_dict()).replace(" nan", " float('nan')"))
        self.outputdata = pd.DataFrame(
            index=self.df.index, columns=util.EXPORT_COLUMNS_ACCOUNT, data=None)

    def convert(self):
        self.outputdata['Date'] = self.df['Datum'].apply(convert2pp.util.convert_date)
        self.outputdata['Value'] = self.df['Bedrag']
        self.outputdata['Transaction Currency'] = 'EUR'
        self.outputdata['Note'] = self.note
        # self.outputdata['Type'][self.df['Omschrijving'].str.contains("Dividendbelasting")] = 'Taxes'
        self.outputdata['Type'][self.df['Omschrijving'].str.contains("Overschrijving beleggingsrekening")] = 'Deposit'


    def write_outputfile(self, outputfile: str):
        self.outputdata.to_csv(outputfile, decimal=".", sep=";")
        print("Wrote output to: " + outputfile)

    def filter_input(self):
        df = self.inputdata

        # exclude this selection
        df = df[~df["Omschrijving"].str.contains('koop')]


        return df


if __name__ == '__main__':
    converter = IngConverterAccount(os.path.dirname(sys.argv[0]) + '\\from_ing_af_en_bij.csv')
    converter.convert()
    filename = os.path.join(os.getcwd(), 'ing_account_converted.csv')
    converter.write_outputfile(filename)

