import unittest
import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp
from degiro2pp.deGiroConverterTrans import DeGiroConverterTrans


class TestdeGiroConverterAccount(unittest.TestCase):

    def test_basic_conversion(self):
        """
        Test if the deposit is converted
        """
        raw_data = {'Datum': {0: Timestamp('2021-03-02 00:00:00')}, 'Tijd': {0: '10:51'},
                    'Product': {0: 'VANGUARD FTSE AW'}, 'ISIN': {0: 'IE00B3RBWM25'}, 'Beurs': {0: 'EAM'},
                    'Uitvoeringsplaats': {0: 'XAMS'}, 'Aantal': {0: 16}, 'Koers': {0: 91.61}, 'Unnamed: 8': {0: 'EUR'},
                    'Lokale waarde': {0: -1465.76}, 'Unnamed: 10': {0: 'EUR'}, 'Waarde': {0: -1465.76},
                    'Unnamed: 12': {0: 'EUR'}, 'Wisselkoers': {0: 0.0, 'Transactiekosten': 0.0},
                    'Unnamed: 15': {0: float('nan')}, 'Totaal': {0: -1465.76}, 'Unnamed: 17': {0: 'EUR'},
                    'Order ID': {0: '1bd0199c-a7c2-40c1-989a-0e6e09958e6e'}}

        df = pd.DataFrame.from_dict(raw_data)
        converter = DeGiroConverterTrans(data=df)
        converter.convert()

        result = converter.outputdata.iloc[0]
        self.assertEqual(result['shares'], 16)
        self.assertEqual(result['Transaction Currency'], 'EUR')


if __name__ == '__main__':
    unittest.main()
