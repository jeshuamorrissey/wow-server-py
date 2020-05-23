import argparse
import logging
from typing import Text

import coloredlogs

from database import db


def main(db_file: Text):
    coloredlogs.install(level=logging.DEBUG)
    db.SetupDatabase(db_file=db_file)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--db_file',
                            type=str,
                            required=True,
                            help='The absolute path to the project base directory.')

    args = arg_parser.parse_args()
    main(args.db_file)
