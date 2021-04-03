import unittest
import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp
from degiro2pp.deGiroConverterAccount import DeGiroConverterAccount


class TestdeGiroConverterAccount(unittest.TestCase):

    def test_deposit(self):
        """
        Test if the deposit is converted
        """
        raw_data = {'Datum': {0: Timestamp('2020-12-02 00:00:00'), 1: Timestamp('2020-12-02 00:00:00'),
                              2: Timestamp('2020-12-01 00:00:00'), 3: Timestamp('2020-11-18 00:00:00')},
                    'Tijd': {0: '17:00', 1: '17:00', 2: '11:43', 3: '17:07'},
                    'Valutadatum': {0: '01-12-2020', 1: '01-12-2020', 2: '01-12-2020', 3: '07-09-2020'},
                    'Product': {0: float('nan'), 1: float('nan'), 2: float('nan'), 3: 'VANGUARD TOTAL STOCK M'},
                    'ISIN': {0: float('nan'), 1: float('nan'), 2: float('nan'), 3: 'US9229087690'},
                    'Omschrijving': {0: 'iDEAL Deposit', 1: 'Reservation iDEAL / Sofort Deposit',
                                     2: 'Reservation iDEAL / Sofort Deposit', 3: 'Dividendbelasting'},
                    'FX': {0: float('nan'), 1: float('nan'), 2: float('nan'), 3: float('nan')},
                    'Mutatie': {0: 'EUR', 1: 'EUR', 2: 'EUR', 3: 'USD'},
                    'Unnamed: 8': {0: '2000.00', 1: '-2000.00', 2: '2000.00', 3: '-0.01'},
                    'Saldo': {0: 'EUR', 1: 'EUR', 2: 'EUR', 3: 'USD'},
                    'Unnamed: 10': {0: '65.92', 1: '-1934.08', 2: '2132.80', 3: '2.28'},
                    'Order Id': {0: float('nan'), 1: float('nan'), 2: float('nan'), 3: float('nan')}}
        df = pd.DataFrame(raw_data, columns=['Datum',
                                             'Tijd',
                                             'Valutadatum',
                                             'Product',
                                             'ISIN',
                                             'Omschrijving',
                                             'FX',
                                             'Mutatie',
                                             'Unnamed: 8',
                                             'Saldo',
                                             'Unnamed: 10',
                                             'Order Id'
                                             ])
        converter = DeGiroConverterAccount(data=df)
        converter.convert()

        deposit = converter.outputdata[converter.outputdata['Type'] == 'Deposit']

        self.assertEqual(deposit['Value'][0], 2000.00)
        self.assertEqual(len(deposit), 1)

    def test_currency_conversion(self):
        """
        Test if the currency is converted correctly
        original amount: 79.11 USD
        Conversion rate 2020-10-07 : 1.1053
        New amount: 71,57 EUR
        """
        raw_data = {'Datum': {0: Timestamp('2020-10-17 00:00:00')}, 'Tijd': {0: '07:41'},
                    'Valutadatum': {0: '17-10-2021'}, 'Product': {0: float('nan')}, 'ISIN': {0: 'IE00B3RBWM25'},
                    'Omschrijving': {0: 'iDEAL Deposit'}, 'FX': {0: float('nan')}, 'Mutatie': {0: 'EUR'},
                    'Unnamed: 8': {0: 79.11}, 'Saldo': {0: 'USD'}, 'Unnamed: 10': {0: 37.49},
                    'Order Id': {0: '123'}}
        df = pd.DataFrame.from_dict(raw_data)
        converter = DeGiroConverterAccount(data=df)
        converter.convert()
        converted = converter.outputdata[converter.outputdata['ISIN'] == 'IE00B3RBWM25']
        self.assertEqual(converted['Value'].iloc[0], 71.57)

    def test_date(self):
        """
        Test date conversion
        """
        raw_data = {'Datum': {0: Timestamp('2021-02-17 00:00:00')}, 'Tijd': {0: '07:41'},
                    'Valutadatum': {0: '16-02-2021'}, 'Product': {0: float('nan')}, 'ISIN': {0: float('nan')},
                    'Omschrijving': {0: 'iDEAL Deposit'}, 'FX': {0: float('nan')}, 'Mutatie': {0: 'EUR'},
                    'Unnamed: 8': {0: 1500.0}, 'Saldo': {0: 'EUR'}, 'Unnamed: 10': {0: 37.49},
                    'Order Id': {0: '123'}}
        df = pd.DataFrame.from_dict(raw_data)
        converter = DeGiroConverterAccount(data=df)
        converter.convert()
        entry = converter.outputdata.iloc[0]
        self.assertEqual(entry['Date'], '2021-2-17')


if __name__ == '__main__':
    unittest.main()
