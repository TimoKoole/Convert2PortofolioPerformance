import unittest

import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp

from convert2pp.ingConverterAccount import IngConverterAccount


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

    def test_bug_2022_05_20(self):
        """
        Fee is not shown as fee and shown twice, once as + once as -. expect only once and with type fees
        """
        raw_data = {'Datum': {1: Timestamp('2022-05-10 00:00:00'), 3: Timestamp('2022-05-05 00:00:00'),
                              4: Timestamp('2022-04-30 00:00:00'), 5: Timestamp('2022-04-30 00:00:00')},
                    'Omschrijving': {1: 'Overschrijving beleggingsrekening', 3: 'Overschrijving beleggingsrekening',
                                     4: 'Basisfee en/of Servicefee rekening 14086338 01/01/2022 - 31/03/2022 (nadere specificatie zie afschrift).',
                                     5: 'Kosten beleggen 14086338, 01/01/2022 - 31/03/2022'},
                    'Rekeningtype': {1: 'Gelddeel', 3: 'Gelddeel', 4: 'Gelddeel', 5: 'Gelddeel'},
                    'Valuta': {1: '€', 3: '€', 4: '€', 5: '€'}, 'Bedrag': {1: 1000.0, 3: 1500.0, 4: -13.27, 5: 13.27},
                    'Tegenrekening': {1: float('nan'), 3: float('nan'), 4: float('nan'), 5: float('nan')},
                    'Transactienummer': {1: 311875017, 3: 311718143, 4: 311268231, 5: 311243103},
                    'Waarderingsdatum': {1: '10-05-2022', 3: '05-05-2022', 4: '30-04-2022', 5: '30-04-2022'},
                    'ING kosten valuta': {1: '¤', 3: '¤', 4: '¤', 5: '¤'},
                    'ING kosten': {1: 0.0, 3: 0.0, 4: 0.0, 5: 0.0},
                    'Belasting valuta': {1: '¤', 3: '¤', 4: '€', 5: '¤'},
                    'Belasting': {1: 0.0, 3: 0.0, 4: 13.27, 5: 0.0}}

        df = pd.DataFrame(raw_data)
        converter = IngConverterAccount(data=df)
        converter.convert()

        self.assertEqual(converter.outputdata[converter.outputdata['Type'] == 'Fees'].shape[0], 1)
        self.assertEqual(converter.outputdata[converter.outputdata['Type'].isna()].shape[0], 0)
        self.assertEqual(converter.outputdata[converter.outputdata['Type'] == 'Fees'].iloc[0]['Value'], -13.27)
        self.assertEqual(converter.outputdata[converter.outputdata['Type'] == 'Deposit']['Value'].sum(), 2513.27)

if __name__ == '__main__':
    unittest.main()
