import argparse


def parse(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-L', '--debug', choices=['INFO', 'WARNING', 'DEBUG'], default='INFO', dest='debug',
                        help="Debug level", required=False)
    parser.set_defaults(debug='INFO')
    return parser.parse_args(argv)
