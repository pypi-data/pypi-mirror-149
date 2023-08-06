import argparse


def parse(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-L', '--debug', choices=['INFO', 'WARNING', 'DEBUG'], default='INFO', dest='debug',
                        help="Debug level", required=False)
    parser.add_argument('-C', '--configuration', dest='configuration', default='/opt/configuration',
                        help="""Using folder '/opt/configuration' if omitted (within docker)""")
    parser.add_argument('-V', '--version', dest='version', action='store_true')
    parser.set_defaults(debug='INFO', version=False)
    return parser.parse_args(argv)
