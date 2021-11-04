import sys
import os
import pandas as pd
import convert2pp.util as util
import datetime


def dateparse(x): return datetime.datetime.strptime(x, '%d-%m-%Y')


class IngConverterTrans:

    def __init__(self, inputfile: str = None, data=None):
        if data is None:
            self.inputdata = pd.read_csv(inputfile,
                                         decimal=",",
                                         delimiter="\t",
                                         parse_dates=[0],
                                         date_parser=dateparse,
                                         encoding = 'UTF-16LE')
        else:
            self.inputdata = data
        print(str(self.inputdata.to_dict()).replace(" nan", " float('nan')"))
        self.outputdata = pd.DataFrame(
            index=self.inputdata.index, columns=util.EXPORT_COLUMNS_TRANSACTIONS, data=None)
        self.note = 'Timo import at: ' + str(datetime.datetime.now())

    def convert(self):
        self.outputdata['Date'] = self.inputdata['Datum'].apply(util.convert_date)
        self.outputdata['ISIN'] = self.inputdata['Naam'].apply(convert_isin)
        self.outputdata['shares'] = self.inputdata['Aantal']
        self.outputdata['Fees'] = 0
        self.outputdata['Value'] = self.inputdata['Waarde'].fillna(0.0)
        self.outputdata['Transaction Currency'] = 'EUR'
        self.outputdata['Exchange Rate'] = 0.0
        self.outputdata['Note'] = self.note

    def write_outputfile(self, outputfile: str):
        self.outputdata.to_csv(outputfile, decimal=".", sep=";")
        print("Wrote output to: " + outputfile)

def convert_isin(name:str):
    if "orthern Trust World Custom Index Fund" in name:
        return "NL0011225305"
    else:
        return ""


if __name__ == '__main__':
    converter = IngConverterTrans(
        os.path.dirname(sys.argv[0]) + '\\from_ing_transactions.csv')
    converter.convert()
    filename = os.path.join(os.getcwd(), 'ing_transactions_converted.csv')
    converter.write_outputfile(filename)
