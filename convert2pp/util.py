def convert_date(date):
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    return year + '-' + month + '-' + day


EXPORT_COLUMNS_TRANSACTIONS = ["Date", "ISIN", "Value", "Shares",
                               "Fees", "Taxes", 'Transaction Currency', 'Exchange Rate', 'Type', 'Notes']

EXPORT_COLUMNS_ACCOUNT = ["Date", "Value",
                          "Shares", "Fees", 'Transaction Currency', 'Type']
