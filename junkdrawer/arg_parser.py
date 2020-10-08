"""A clean and organized way to have an argument parser for a script"""


import argparse


def _get_argparser():
    """to organize and clean format argparser args"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--arg_1",
        action="store",
        dest="arg_1",
        default="default_arg_1",
        help="help message"
    )

    parser.add_argument(
        "--arg_2",
        action="store",
        dest="arg_2",
        default="default_arg_2",
        help="help message"
    )

    #         .
    # (and any more arguments)
    #         .

    # mutuall exclusive args

    mutually_exclusive_args = parser.add_mutually_exclusive_group()

    mutually_exclusive_args.add_argument(
        "--me_arg_1",
        action="store",
        dest="me_arg_1",
        default="default_me_arg_1",
        help="help message"    
    )

    mutually_exclusive_args.add_argument(
        "--me_arg_2",
        action="store",
        dest="me_arg_2",
        default="default_me_arg_2",
        help="help message"    
    )

    #         .
    # (and any more mutually exlusive arguments)
    #         .

    # catch all 'vars' argument for user to list any other field/values parameters
    parser.add_argument(
        "--vars",
        action="store",
        dest="vars",
        nargs="*",
        default=None,
        help="Any additional variables that do not have explicit command line options. Supply as a list in form: '--vars var1=val1 var2=val2 ..."
    )

    return parser


def main():

    parser = _get_argparser()

    # parse all args and put in dict
    options = vars(parser.parse_args())

    #         .
    # Rest of script
    #         .


    return


if __name__ == "__main__":
        main()

