import argparse
import os

from degiro2pp.deGiroConverterAccount import DeGiroConverterAccount

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input file, default Account.csv', type=str, nargs='?',
                        default=os.path.join(os.getcwd(), "Account.csv"))
    parser.add_argument('-o', '--output', help='output file, default degiro_account_converted.csv', type=str, nargs='?',
                        default=os.path.join(os.getcwd(), "degiro_account_converted.csv"))
    args = parser.parse_args()
    print("Converting file:" + args.input)

    converter = DeGiroConverterAccount(args.input)
    converter.convert()
    converter.write_outputfile(outputfile=args.output)
