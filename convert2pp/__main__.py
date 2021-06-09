import argparse
import os
from datetime import date

from convert2pp.deGiroConverterAccount import DeGiroConverterAccount
from convert2pp.deGiroConverterTrans import DeGiroConverterTrans
from convert2pp.ingConverterAccount import IngConverterAccount
from convert2pp.ingConverterTrans import IngConverterTrans

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input file, default Account.csv', type=str, nargs='?',
                        default=os.path.join(os.getcwd(), "Account.csv"))
    parser.add_argument('-o', '--output', help='output file, default date + degiro_converted.csv', type=str, nargs='?',
                        default=os.path.join(os.getcwd(), str(date.today()) + 'degiro_converted.csv'))
    parser.add_argument('-t', '--type', help='file input type, default account', type=str, nargs='?',
                        choices=['account', 'transactions'], default='account')
    parser.add_argument('-b', '--broker', help='boker , default degiro', type=str, nargs='?',
                        choices=['degiro', 'ing'], default='account')
    args = parser.parse_args()
    print("Converting file:" + args.input)

    if args.broker == 'degiro':
        if args.type == 'account':
            converter = DeGiroConverterAccount(args.input)
        elif args.type == 'transactions':
            converter = DeGiroConverterTrans(args.input)

    if args.broker == 'ing':
        if args.type == 'account':
            converter = IngConverterAccount(args.input)
        elif args.type == 'transactions':
            converter = IngConverterTrans(args.input)
    converter.convert()
    converter.write_outputfile(outputfile=args.output)
