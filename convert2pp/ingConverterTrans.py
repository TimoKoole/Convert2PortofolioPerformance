import datetime
import os
import sys

import pandas as pd

import convert2pp.util as util


def dateparse(x): return datetime.datetime.strptime(x, '%d-%m-%Y')


class IngConverterTrans:

    def __init__(self, inputfile: str = None, data=None):
        if data is None:
            self.inputdata = pd.read_csv(inputfile,
                                         decimal=",",
                                         delimiter="\t",
                                         parse_dates=[0],
                                         date_parser=dateparse,
                                         encoding='UTF-16LE')
        else:
            self.inputdata = data
        # print(str(self.inputdata.to_dict()).replace(" nan", " float('nan')"))
        self.inputdata = filter_input(self.inputdata)
        self.outputdata = pd.DataFrame(
            index=self.inputdata.index, columns=util.EXPORT_COLUMNS_TRANSACTIONS, data=None)
        self.note = 'convert2pp import at: ' + str(datetime.datetime.now())

    def convert(self):
        self.outputdata['Date'] = self.inputdata['Datum'].apply(util.convert_date)
        self.outputdata['ISIN'] = self.inputdata['Naam'].apply(convert_isin)
        self.outputdata['Shares'] = self.inputdata['Aantal']
        self.outputdata['Taxes'] = self.inputdata['Belasting']
        self.outputdata['Value'] = self.inputdata['Notabedrag'].fillna(0.0)
        self.outputdata['Transaction Currency'] = 'EUR'
        self.outputdata['Exchange Rate'] = 0.0
        self.outputdata['Note'] = self.note
        self.outputdata['Type'] = self.inputdata['Type'].apply(convert_type)

    def write_outputfile(self, outputfile: str):
        self.outputdata.to_csv(outputfile, decimal=".", sep=";")
        print("Wrote output to: " + outputfile)


def convert_isin(name: str):
    if "orthern Trust World Custom Index Fund" in name or "Northern Trust WC" in name  :
        return "NL0011225305"
    elif "Northern Trust EM" in name:
        return "NL0011515424"
    else:
        return ""


def convert_type(name: str):
    if name == 'K':
        return 'Buy'
    elif name == 'UITK':
        return 'Dividend'
    else:
        return ''


def filter_input(df):
    # exclude this selection
    try:
        df = df[~df["Type"].str.contains('TOEK')]
    except KeyError as e:
        print("Failed to exclude buy orders")
        print(df)
        raise e

    return df


# https://mijn.ing.nl/investments/portfolio-transactions/
if __name__ == '__main__':
    converter = IngConverterTrans(
        os.path.dirname(
            sys.argv[0]) + '/portfolio_transaction_overview_14086339-100-1-14086338_2023-06-01_2023-07-09.csv')
    converter.convert()
    filename = os.path.join(os.getcwd(), 'ing_transactions_converted.csv')
    converter.write_outputfile(filename)
