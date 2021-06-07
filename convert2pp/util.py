def convert_date(date):
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    return year + '-' + month + '-' + day

EXPORT_COLUMNS_TRANSACTIONS = ["Date", "ISIN", "Value", "shares",
                      "Fees", 'Transaction Currency', 'Exchange Rate', 'Type', 'Notes']

EXPORT_COLUMNS_ACCOUNT = ["Date", "ISIN", "Value",
                          "shares", "Fees", 'Transaction Currency', 'Type']
