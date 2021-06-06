import unittest
import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp
from degiro2pp.ingConverterAccount import IngConverterAccount


class TestIngConverterAccountt(unittest.TestCase):

    def test_deposit(self):
        """
        Test if the deposit is converted
        """
        raw_data = {'Datum': {1: Timestamp('2021-06-01 00:00:00')},
                    'Omschrijving': {1: 'Overschrijving beleggingsrekening'}, 'Valuta': {1: 'EUR'},
                    'Rekeningtype': {1: 'Gelddeel'}, 'Bedrag': {1: 1500}, 'Transactienummer': {1: 296640628},
                    'Valutadatum': {1: '2021-06-01'}, 'ING kosten': {1: 0}, 'Belasting': {1: 0},
                    'Rekeningnummer van': {1: 'Uw Betaalrekening'}, 'Rekeningnummer naar': {1: 14086338.0}}

        df = pd.DataFrame(raw_data)
        converter = IngConverterAccount(data=df)
        converter.convert()

        deposit = converter.outputdata[converter.outputdata['Type'] == 'Deposit']

        self.assertEqual(deposit['Value'][1], 1500.00)
        self.assertEqual(len(deposit), 1)


if __name__ == '__main__':
    unittest.main()
