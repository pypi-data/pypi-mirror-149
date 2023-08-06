from configparser import ConfigParser
from chela.formula_handler import check_formula, build_dataframe
import argparse
import pandas as pd

def main():
    #Define the parser
    my_parser = argparse.ArgumentParser(prog='chela',
                                        description = "Handle chemical formulas",
                                        usage = '%(prog)s [options]',
                                        )
    #Add option -c to use check_formula function
    my_parser.add_argument('-check',
                          action= 'store',
                          metavar=('formula'),
                          help="Check correctness chemical formula",
                          )

    #Add option -d to use build_dataframe function
    my_parser.add_argument('-dataframe',
                           nargs=2,
                           metavar=('SOURCE','NAME'),
                           action='store',
                           help="Transform chemical formula into dataframe Source Name",
                           )

    #Parse the args
    args = my_parser.parse_args()

    if args.check:
        print('Checking...')
        check_formula(args.check)
        print('Correct formula.')

    elif args.dataframe:
        print('Transforming file into a Dataframe...')
        source, destination = args.dataframe
        dataset = pd.read_csv(source)
        dataframe = build_dataframe(dataset)
        dataframe.to_csv(destination,index=False)
        print('Dataframe saved.')



if __name__ == "__main__":
    main()
