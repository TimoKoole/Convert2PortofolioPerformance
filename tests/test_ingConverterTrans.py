import unittest

import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp

from convert2pp.ingConverterTrans import IngConverterTrans


class TestdeINGConverterTrans(unittest.TestCase):
    def test_transaction(self):
        """
        Test if the transaction is converted
        """
        raw_data = {
            "Datum": {0: Timestamp("2021-06-04 00:00:00")},
            "Naam": {0: "Northern Trust World Custom Index Fund"},
            "Aantal": {0: 83.595},
            "Type": {0: "K"},
            "Waarde valuta": {0: "€"},
            "Waarde": {0: -1500.0},
            "Gerealiseerd rendement valuta": {0: "€"},
            "Gerealiseerd rendement": {0: 0.0},
            "Koers valuta": {0: "€"},
            "Koers": {0: 17.944},
            "Wisselkoers": {0: float("nan")},
            "Nummer": {0: 297023132},
            "Via": {0: "Internet"},
            "Transactiedatum": {0: "04-06-2021"},
            "Valutadatum": {0: "07-06-2021"},
            "Boekdatum": {0: "04-06-2021"},
            "Settlementdatum": {0: "07-06-2021"},
            "Orderbedrag valuta": {0: "€"},
            "Orderbedrag": {0: 1500.0},
            "ING kosten valuta": {0: "¤"},
            "ING kosten": {0: 0.0},
            "Belasting valuta": {0: "¤"},
            "Belasting": {0: 0.0},
            "Notabedrag valuta": {0: "€"},
            "Notabedrag": {0: 1500.0},
            "Rente methode": {0: float("nan")},
            "Rentedagen": {0: float("nan")},
            "Opgelopen rente valuta": {0: float("nan")},
            "Opgelopen rente": {0: float("nan")},
        }

        df = pd.DataFrame.from_dict(raw_data)
        converter = IngConverterTrans(data=df)
        converter.convert()

        result = converter.outputdata
        self.assertEqual(result["Shares"][0], 83.595)
        self.assertEqual(result["Transaction Currency"][0], "EUR")

    def test_bug_2022_05_21(self):
        """
        Emerging market ETF does not show up in the end
        """
        raw_data = {
            "Datum": {
                0: Timestamp("2022-05-12 00:00:00"),
                1: Timestamp("2022-05-11 00:00:00"),
                2: Timestamp("2022-05-09 00:00:00"),
            },
            "Naam": {
                0: "Northern Trust World Custom Index Fund",
                1: "Northern Trust EM Custom ESG Eq Idx Fund",
                2: "Northern Trust EM Custom ESG Eq Idx Fund",
            },
            "Aantal": {0: 54.609, 1: 201.918, 2: 105.933},
            "Type": {0: "K", 1: "TOEK", 2: "K"},
            "Waarde valuta": {0: "€", 1: "€", 2: "€"},
            "Waarde": {0: -1000.0, 1: 0.0, 2: -1500.0},
            "Gerealiseerd rendement valuta": {0: "€", 1: "€", 2: "€"},
            "Gerealiseerd rendement": {0: 0.0, 1: 0.0, 2: 0.0},
            "Koers valuta": {0: "€", 1: "€", 2: "€"},
            "Koers": {0: 18.312, 1: 0.0, 2: 14.16},
            "Wisselkoers": {0: float("nan"), 1: float("nan"), 2: float("nan")},
            "Nummer": {0: 311987495, 1: 312163962, 2: 311853360},
            "Via": {0: "Internet", 1: "Regulier", 2: "Internet"},
            "Transactiedatum": {0: "12-05-2022", 1: "11-05-2022", 2: "09-05-2022"},
            "Valutadatum": {0: "13-05-2022", 1: "11-05-2022", 2: "10-05-2022"},
            "Boekdatum": {0: "12-05-2022", 1: "17-05-2022", 2: "09-05-2022"},
            "Afwikkelingsdatum": {0: "13-05-2022", 1: "11-05-2022", 2: "10-05-2022"},
            "Orderbedrag valuta": {0: "€", 1: "€", 2: "€"},
            "Orderbedrag": {0: 1000.0, 1: 0.0, 2: 1500.0},
            "ING kosten valuta": {0: "¤", 1: "¤", 2: "¤"},
            "ING kosten": {0: 0.0, 1: 0.0, 2: 0.0},
            "Belasting valuta": {0: "¤", 1: "¤", 2: "¤"},
            "Belasting": {0: 0.0, 1: 0.0, 2: 0.0},
            "Notabedrag valuta": {0: "€", 1: "€", 2: "€"},
            "Notabedrag": {0: 1000.0, 1: 0.0, 2: 1500.0},
            "Rente methode": {0: float("nan"), 1: float("nan"), 2: float("nan")},
            "Rentedagen": {0: float("nan"), 1: float("nan"), 2: float("nan")},
            "Opgelopen rente valuta": {
                0: float("nan"),
                1: float("nan"),
                2: float("nan"),
            },
            "Opgelopen rente": {0: float("nan"), 1: float("nan"), 2: float("nan")},
        }

        df = pd.DataFrame.from_dict(raw_data)
        converter = IngConverterTrans(data=df)
        converter.convert()

        result = converter.outputdata
        self.assertEqual(
            result[result["ISIN"] == "NL0011515424"].iloc[0]["Value"], 1500
        )

    def test_bug_2023_03_27(self):
        """
        ETF name change failed to resolve
        """
        raw_data = {
            "Datum": {0: Timestamp("2021-06-04 00:00:00")},
            "Naam": {0: "Northern Trust WC ESG EI UCITS FGR Fe Fd"},
            "Aantal": {0: 83.595},
            "Type": {0: "K"},
            "Belasting": {0: 0.0},
            "Notabedrag": {0: 1500.0},
        }

        df = pd.DataFrame.from_dict(raw_data)
        converter = IngConverterTrans(data=df)
        converter.convert()

        result = converter.outputdata
        self.assertEqual(result.iloc[0]["ISIN"], "NL0011225305")


if __name__ == "__main__":
    unittest.main()
