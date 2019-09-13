import sys
import os
import pandas as pd
import util


class DeGiroConverterAccount:
    EXPORT_COLUMNS = ["Date", "ISIN", "value",
                      "shares", "Fees", 'Transaction Currency']

    def __init__(self, inputfile):
        def dateparse(x): return pd.datetime.strptime(x, '%d-%m-%Y')
        self.inputdata = pd.read_csv(inputfile, parse_dates=[
                                     0], date_parser=dateparse)
        self.df = self.filter_input()
        self.outputdata = pd.DataFrame(
            index=self.df.index, columns=self.EXPORT_COLUMNS, data=None)

    def convert(self):
        self.outputdata['Date'] = self.df['Datum'].apply(util.convert_date)
        self.outputdata['ISIN'] = self.df['ISIN']
        self.outputdata['value'] = self.df.iloc[:, 8]
        self.outputdata['Transaction Currency'] = self.df['Mutatie']

    def write_outputfile(self, outputfolder, outputfile):
        os.makedirs(outputfolder, exist_ok=True)
        self.outputdata.to_csv(os.path.join(
            outputfolder, outputfile), decimal=",", sep=",")

    def filter_input(self):
        df = self.inputdata
        df = df[(df['Omschrijving'] == "Dividend") | (
            df['Omschrijving'] == "iDEAL storting")]
        return df


if __name__ == '__main__':
    converter = DeGiroConverterAccount(
        os.path.dirname(sys.argv[0]) + '\\Account.csv')
    converter.convert()
    converter.write_outputfile(os.path.dirname(
        sys.argv[0]), 'degiro_account_converted.csv')
