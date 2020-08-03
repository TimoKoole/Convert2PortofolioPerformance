import sys
import os
import pandas as pd
import degiro.util as util
import datetime


class DeGiroConverterTrans:

    EXPORT_COLUMNS = ["Date", "ISIN", "Value", "shares",
                      "Fees", 'Transaction Currency', 'Exchange Rate', 'Type', 'Notes']

    def __init__(self, inputfile):
        def dateparse(x): return pd.datetime.strptime(x, '%d-%m-%Y')
        self.inputdata = pd.read_csv(inputfile, parse_dates=[
                                     0], date_parser=dateparse)
        self.outputdata = pd.DataFrame(
            index=self.inputdata.index, columns=self.EXPORT_COLUMNS, data=None)
        self.note = 'Timo import at: ' + str(datetime.datetime.now())

    def convert(self):
        self.outputdata['Date'] = self.inputdata['Datum'].apply(util.convert_date)
        self.outputdata['ISIN'] = self.inputdata['ISIN']
        self.outputdata['shares'] = self.inputdata['Aantal']
        self.outputdata['Fees'] = self.inputdata.iloc[:, 14]
        self.outputdata['Value'] = self.inputdata.iloc[:, 9]
        self.outputdata['Transaction Currency'] = 'EUR'
        self.outputdata['Transaction Currency'] = self.inputdata['Lokale waarde']
        self.outputdata['Exchange Rate'] = self.inputdata['Wisselkoers']





    def write_outputfile(self, outputfolder, outputfile):
        os.makedirs(outputfolder, exist_ok=True)
        self.outputdata.to_csv(os.path.join(
            outputfolder, outputfile), decimal=",", sep=";")


if __name__ == '__main__':
    converter = DeGiroConverterTrans(
        os.path.dirname(sys.argv[0]) + '\\Transactions.csv')
    converter.convert()
    converter.write_outputfile(os.path.dirname(
        sys.argv[0]), 'degiro_portofolio_converted.csv')
