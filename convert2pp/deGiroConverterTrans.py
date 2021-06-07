import sys
import os
import pandas as pd
import convert2pp.util as util
import datetime


def dateparse(x): return datetime.datetime.strptime(x, '%d-%m-%Y')


class DeGiroConverterTrans:

    def __init__(self, inputfile: str = None, data=None):
        if data is None:
            self.inputdata = pd.read_csv(inputfile, parse_dates=[ 0], date_parser=dateparse)
        else:
            self.inputdata = data
        # print(str(self.inputdata.to_dict()).replace(" nan", " float('nan')"))
        self.outputdata = pd.DataFrame(
            index=self.inputdata.index, columns=util.EXPORT_COLUMNS_TRANSACTIONS, data=None)
        self.note = 'Timo import at: ' + str(datetime.datetime.now())

    def convert(self):
        self.outputdata['Date'] = self.inputdata['Datum'].apply(util.convert_date)
        self.outputdata['ISIN'] = self.inputdata['ISIN']
        self.outputdata['shares'] = self.inputdata['Aantal']
        self.outputdata['Fees'] = self.inputdata.iloc[:, 14]
        self.outputdata['Value'] = self.inputdata['Waarde'].fillna(0.0)
        self.outputdata['Transaction Currency'] = self.inputdata.iloc[:, 10]
        self.outputdata['Exchange Rate'] = self.inputdata['Wisselkoers']

    def write_outputfile(self, outputfile: str):
        self.outputdata.to_csv(outputfile, decimal=".", sep=";")
        print("Wrote output to: " + outputfile)


if __name__ == '__main__':
    converter = DeGiroConverterTrans(
        os.path.dirname(sys.argv[0]) + '\\Transactions.csv')
    converter.convert()
    converter.write_outputfile(os.path.dirname(
        sys.argv[0]), 'degiro_portofolio_converted.csv')
