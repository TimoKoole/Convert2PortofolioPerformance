import argparse
import os
from datetime import date

from degiro2pp.deGiroConverterAccount import DeGiroConverterAccount
from degiro2pp.deGiroConverterTrans import DeGiroConverterTrans

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input file, default Account.csv', type=str, nargs='?',
                        default=os.path.join(os.getcwd(), "Account.csv"))
    parser.add_argument('-o', '--output', help='output file, default date + degiro_converted.csv', type=str, nargs='?',
                        default=os.path.join(os.getcwd(), str(date.today()) + 'degiro_converted.csv'))
    parser.add_argument('-t', '--type', help='file input type, default account', type=str, nargs='?',
                        choices=['account', 'transactions'], default='account')
    args = parser.parse_args()
    print("Converting file:" + args.input)

    if args.type == 'account':
        converter = DeGiroConverterAccount(args.input)
    elif args.type == 'transactions':
        converter = DeGiroConverterTrans(args.input)
    converter.convert()
    converter.write_outputfile(outputfile=args.output)
