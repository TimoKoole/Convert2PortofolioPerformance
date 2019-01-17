import sys
import os
import pandas as pd

EXPORT_COLUMNS = ["Date", "ISIN", "value", "shares", "Fees", 'Transaction Currency', 'Exchange Rate']

def convert_date(date):
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    return year + '-' + month + '-' + day


class DeGiroConverterTrans():
    def __init__(self, inputfile):
        self.inputdata = pd.read_csv(inputfile, parse_dates=[0])
        self.outputdata = pd.DataFrame(
            index=self.inputdata.index, columns=EXPORT_COLUMNS, data=None )

    def convert(self):
        self.filter()
        
        self.outputdata['Date'] = self.inputdata['Datum'].apply(convert_date)
        self.outputdata['ISIN'] = self.inputdata['ISIN']
        self.outputdata['shares'] = self.inputdata['Aantal']
        self.outputdata['Fees'] = self.inputdata.iloc[:, 14]
        self.outputdata['value'] = self.inputdata.iloc[:, 7]

        self.outputdata['Transaction Currency'] = 'EUR'
        self.outputdata['Exchange Rate'] = self.inputdata['Wisselkoers']


    def write_outputfile(self, outputfolder, outputfile):
        os.makedirs(outputfolder, exist_ok=True)
        self.outputdata.to_csv(os.path.join(outputfolder, outputfile), decimal=",", sep=";")

    def filter(self):
        self.inputdata = self.inputdata.loc[self.inputdata['ISIN'] != '']


if __name__ == '__main__':
    converter = DeGiroConverterTrans(os.path.dirname(sys.argv[0]) + '\\Transactions.csv')
    converter.convert()
    converter.write_outputfile( os.path.dirname(sys.argv[0]),'degiro_converted.csv' )