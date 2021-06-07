import unittest
import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp
from convert2pp.ingConverterTrans import IngConverterTrans


class TestdeINGConverterTrans(unittest.TestCase):

    def test_transaction(self):
        """
        Test if the transaction is converted
        """
        raw_data = {'Datum': {0: Timestamp('2021-06-04 00:00:00')},
                    'Naam': {0: 'Northern Trust World Custom Index Fund'}, 'Aantal': {0: 83.595}, 'Type': {0: 'K'},
                    'Waarde valuta': {0: '€'}, 'Waarde': {0: -1500.0}, 'Gerealiseerd rendement valuta': {0: '€'},
                    'Gerealiseerd rendement': {0: 0.0}, 'Koers valuta': {0: '€'}, 'Koers': {0: 17.944},
                    'Wisselkoers': {0: float('nan')}, 'Nummer': {0: 297023132}, 'Via': {0: 'Internet'},
                    'Transactiedatum': {0: '04-06-2021'}, 'Valutadatum': {0: '07-06-2021'},
                    'Boekdatum': {0: '04-06-2021'}, 'Settlementdatum': {0: '07-06-2021'},
                    'Orderbedrag valuta': {0: '€'}, 'Orderbedrag': {0: 1500.0}, 'ING kosten valuta': {0: '¤'},
                    'ING kosten': {0: 0.0}, 'Belasting valuta': {0: '¤'}, 'Belasting': {0: 0.0},
                    'Notabedrag valuta': {0: '€'}, 'Notabedrag': {0: 1500.0}, 'Rente methode': {0: float('nan')},
                    'Rentedagen': {0: float('nan')}, 'Opgelopen rente valuta': {0: float('nan')},
                    'Opgelopen rente': {0: float('nan')}}

        df = pd.DataFrame.from_dict(raw_data)
        converter = IngConverterTrans(data=df)
        converter.convert()

        result = converter.outputdata
        self.assertEqual(result['shares'][0], 83.595)
        self.assertEqual(result['Transaction Currency'][0], 'EUR')


if __name__ == '__main__':
    unittest.main()
