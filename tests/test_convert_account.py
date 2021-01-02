import unittest
import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp
from degiro2pp.deGiroConverterAccount import DeGiroConverterAccount


class TestdeGiroConverterAccount(unittest.TestCase):

    def setUp(self):
        """
        Create test data like this: print(str(self.df.to_dict()).replace(" nan"," float('nan')") )
        """
        raw_data = {'Datum': {1: Timestamp('2020-12-01 00:00:00'), 6: Timestamp('2020-11-18 00:00:00'),
                              7: Timestamp('2020-11-18 00:00:00'), 8: Timestamp('2020-11-18 00:00:00'),
                              9: Timestamp('2020-11-18 00:00:00'), 10: Timestamp('2020-11-18 00:00:00'),
                              11: Timestamp('2020-11-18 00:00:00'), 12: Timestamp('2020-11-18 00:00:00'),
                              13: Timestamp('2020-11-18 00:00:00'), 14: Timestamp('2020-11-18 00:00:00'),
                              15: Timestamp('2020-11-18 00:00:00'), 16: Timestamp('2020-11-18 00:00:00'),
                              17: Timestamp('2020-11-18 00:00:00'), 18: Timestamp('2020-11-18 00:00:00'),
                              19: Timestamp('2020-11-18 00:00:00'), 20: Timestamp('2020-11-18 00:00:00'),
                              21: Timestamp('2020-11-18 00:00:00'), 22: Timestamp('2020-11-18 00:00:00'),
                              51: Timestamp('2020-10-07 00:00:00'), 59: Timestamp('2020-10-01 00:00:00'),
                              60: Timestamp('2020-10-01 00:00:00'), 69: Timestamp('2020-09-24 00:00:00'),
                              70: Timestamp('2020-09-24 00:00:00')},
                    'Tijd': {1: '11:43', 6: '17:07', 7: '17:07', 8: '17:07', 9: '17:07', 10: '17:07', 11: '17:07',
                             12: '17:07', 13: '17:07', 14: '17:07', 15: '17:07', 16: '17:07', 17: '17:07', 18: '17:07',
                             19: '17:07', 20: '17:07', 21: '17:07', 22: '17:07', 51: '08:19', 59: '06:17', 60: '06:17',
                             69: '08:34', 70: '08:34'},
                    'Valutadatum': {1: '01-12-2020', 6: '07-09-2020', 7: '07-09-2020', 8: '07-09-2020', 9: '07-09-2020',
                                    10: '07-09-2020', 11: '07-09-2020', 12: '07-09-2020', 13: '07-09-2020',
                                    14: '07-09-2020', 15: '07-09-2020', 16: '07-09-2020', 17: '07-09-2020',
                                    18: '07-09-2020', 19: '07-09-2020', 20: '07-09-2020', 21: '07-09-2020',
                                    22: '07-09-2020', 51: '07-10-2020', 59: '30-09-2020', 60: '30-09-2020',
                                    69: '24-09-2020', 70: '24-09-2020'},
                    'Product': {1: float('nan'), 6: 'VANGUARD TOTAL STOCK M', 7: 'VANGUARD TOTAL INTERNA',
                                8: 'VANGUARD TOTAL INTERNA', 9: 'VANGUARD TOTAL STOCK M', 10: 'VANGUARD TOTAL BOND MA',
                                11: 'VANGUARD TOTAL BOND MA', 12: 'VANGUARD TOTAL BOND MA',
                                13: 'DEUTSCHE X-TRACKERS MS', 14: 'VANGUARD TOTAL INTERNA',
                                15: 'ISHARES CORE MSCI EMER', 16: 'VANGUARD TOTAL BOND MA',
                                17: 'VANGUARD TOTAL BOND MA', 18: 'VANGUARD TOTAL INTERNA',
                                19: 'VANGUARD TOTAL BOND MA', 20: 'VANGUARD TOTAL INTERNA',
                                21: 'VANGUARD TOTAL BOND MA', 22: 'VANGUARD TOTAL BOND MA', 51: 'VANGUARD FTSE AW',
                                59: 'VANGUARD TOTAL STOCK M', 60: 'VANGUARD TOTAL STOCK M',
                                69: 'VANGUARD TOTAL INTERNA', 70: 'VANGUARD TOTAL INTERNA'},
                    'ISIN': {1: float('nan'), 6: 'US9229087690', 7: 'US9219097683', 8: 'US9219097683',
                             9: 'US9229087690', 10: 'US9219378356', 11: 'US9219378356', 12: 'US9219378356',
                             13: 'US2330512003', 14: 'US9219097683', 15: 'US46434G1031', 16: 'US9219378356',
                             17: 'US9219378356', 18: 'US92203J4076', 19: 'US9219378356', 20: 'US9219097683',
                             21: 'US9219378356', 22: 'US9219378356', 51: 'IE00B3RBWM25', 59: 'US9229087690',
                             60: 'US9229087690', 69: 'US9219097683', 70: 'US9219097683'},
                    'Omschrijving': {1: 'Reservation iDEAL / Sofort Deposit', 6: 'Dividendbelasting',
                                     7: 'Dividendbelasting', 8: 'Dividendbelasting', 9: 'Dividendbelasting',
                                     10: 'Dividendbelasting', 11: 'Dividendbelasting', 12: 'Dividendbelasting',
                                     13: 'Dividendbelasting', 14: 'Dividendbelasting', 15: 'Dividendbelasting',
                                     16: 'Dividendbelasting', 17: 'Dividendbelasting', 18: 'Dividendbelasting',
                                     19: 'Dividendbelasting', 20: 'Dividendbelasting', 21: 'Dividendbelasting',
                                     22: 'Dividendbelasting', 51: 'Dividend', 59: 'Dividend', 60: 'Dividendbelasting',
                                     69: 'Dividend', 70: 'Dividendbelasting'},
                    'FX': {1: float('nan'), 6: float('nan'), 7: float('nan'), 8: float('nan'), 9: float('nan'),
                           10: float('nan'), 11: float('nan'), 12: float('nan'), 13: float('nan'), 14: float('nan'),
                           15: float('nan'), 16: float('nan'), 17: float('nan'), 18: float('nan'), 19: float('nan'),
                           20: float('nan'), 21: float('nan'), 22: float('nan'), 51: float('nan'), 59: float('nan'),
                           60: float('nan'), 69: float('nan'), 70: float('nan')},
                    'Mutatie': {1: 'EUR', 6: 'USD', 7: 'USD', 8: 'USD', 9: 'USD', 10: 'USD', 11: 'USD', 12: 'USD',
                                13: 'USD', 14: 'USD', 15: 'USD', 16: 'USD', 17: 'USD', 18: 'USD', 19: 'USD', 20: 'USD',
                                21: 'USD', 22: 'USD', 51: 'USD', 59: 'USD', 60: 'USD', 69: 'USD', 70: 'USD'},
                    'Unnamed: 8': {1: '2000,00', 6: '-0,01', 7: '-0,21', 8: '-0,10', 9: '0,01', 10: '0,39', 11: '0,40',
                                   12: '0,41', 13: '-0,24', 14: '-0,21', 15: '-0,14', 16: '0,40', 17: '0,41',
                                   18: '-0,01', 19: '0,42', 20: '-0,05', 21: '0,39', 22: '0,42', 51: '79,11',
                                   59: '19,55', 60: '-2,93', 69: '10,49', 70: '-1,57'},
                    'Saldo': {1: 'EUR', 6: 'USD', 7: 'USD', 8: 'USD', 9: 'USD', 10: 'USD', 11: 'USD', 12: 'USD',
                              13: 'USD', 14: 'USD', 15: 'USD', 16: 'USD', 17: 'USD', 18: 'USD', 19: 'USD', 20: 'USD',
                              21: 'USD', 22: 'USD', 51: 'USD', 59: 'USD', 60: 'USD', 69: 'USD', 70: 'USD'},
                    'Unnamed: 10': {1: '2132,80', 6: '2,28', 7: '2,29', 8: '2,50', 9: '2,60', 10: '2,59', 11: '2,20',
                                    12: '1,80', 13: '1,39', 14: '1,63', 15: '1,84', 16: '1,98', 17: '1,58', 18: '1,17',
                                    19: '1,18', 20: '0,76', 21: '0,81', 22: '0,42', 51: '79,11', 59: '16,62',
                                    60: '-2,93', 69: '8,92', 70: '-1,57'},
                    'Order Id': {1: float('nan'), 6: float('nan'), 7: float('nan'), 8: float('nan'), 9: float('nan'),
                                 10: float('nan'), 11: float('nan'), 12: float('nan'), 13: float('nan'),
                                 14: float('nan'), 15: float('nan'), 16: float('nan'), 17: float('nan'),
                                 18: float('nan'), 19: float('nan'), 20: float('nan'), 21: float('nan'),
                                 22: float('nan'), 51: float('nan'), 59: float('nan'), 60: float('nan'),
                                 69: float('nan'), 70: float('nan')}}
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
        self.converter = DeGiroConverterAccount(data=df)
        self.converter.convert()

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
                    'Unnamed: 8': {0: '2000,00', 1: '-2000,00', 2: '2000,00', 3: '-0,01'},
                    'Saldo': {0: 'EUR', 1: 'EUR', 2: 'EUR', 3: 'USD'},
                    'Unnamed: 10': {0: '65,92', 1: '-1934,08', 2: '2132,80', 3: '2,28'},
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

        self.assertEqual(deposit['Value'][0], '2000,00')
        self.assertEqual(len(deposit), 1)

    def test_currency_conversion(self):
        """
        Test if the currency is converted correctly
        original amount: 79.11 USD
        Conversion rate 2020-10-07 : 1.1053
        New amount: 71,57 EUR
        """
        converted = self.converter.outputdata[self.converter.outputdata['ISIN'] == 'IE00B3RBWM25']
        self.assertEqual(converted['Value'].iloc[0], '71,57')


if __name__ == '__main__':
    unittest.main()
