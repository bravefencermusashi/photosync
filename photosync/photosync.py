import json
import os
import re
import shutil
import logging
import argparse
from pathlib import Path

DEFAULT_DATABASE_NAME = '.photosync_db'
PATTERN = re.compile('(IMG|VID)_(\d{4})(\d{2})(\d{2})_')


def create_logger(name):
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)
    logger.addHandler(handler)

    return logger


LOGGER = create_logger(__name__)


def init_db_file(path):
    with open(path, 'w') as db_file:
        db_file.write('{}')
    LOGGER.info('db file initialized')


class DBEntry:
    def __init__(self):
        self.year = None
        self.month = None
        self.day = None
        self.full_name = None


def create_dbentry(filename):
    matcher = PATTERN.search(filename)
    dbentry = None
    if matcher:
        dbentry = DBEntry()
        dbentry.year = matcher.group(2)
        dbentry.month = matcher.group(3)
        dbentry.day = matcher.group(4)
        dbentry.full_name = filename
    return dbentry


class Database:
    def __init__(self, dict_: dict):
        self.dict_ = dict_

    def add_member(self, dbentry: DBEntry):
        dict_year = self.dict_.get(dbentry.year, None)
        if dict_year is None:
            dict_year = self.dict_[dbentry.year] = dict()
        dict_month = dict_year.get(dbentry.month, None)
        if dict_month is None:
            dict_month = dict_year[dbentry.month] = dict()
        list_day = dict_month.get(dbentry.day, None)
        if list_day is None:
            list_day = dict_month[dbentry.day] = list()

        if dbentry.full_name not in list_day:
            res = True
            list_day.append(dbentry.full_name)
        else:
            res = False

        return res


def load_db(path_to_db):
    with open(path_to_db, 'r') as database_json:
        database_json = json.load(database_json)

    return Database(database_json)


def save_db(path_to_db, db: Database):
    with open(path_to_db, 'w') as database_json:
        json.dump(db.dict_, database_json)


def synchronize(src: Path, dest: Path, db: Database):
    for root, dirs, files in os.walk(str(src)):
        root_path = Path(root)
        dest_root = dest / root_path.relative_to(src)
        for filename in files:
            dbentry = create_dbentry(str((root_path / filename).relative_to(src)))
            if dbentry and db.add_member(dbentry):
                if not dest_root.exists():
                    dest_root.mkdir()
                shutil.copy2(os.path.join(root, filename), str(dest_root))
                LOGGER.info('file %s copied', dbentry.full_name)


def get_db_path_default():
    return os.path.join(os.path.expanduser('~'), DEFAULT_DATABASE_NAME)


def create_arg_parser():
    parser = argparse.ArgumentParser(prog='photosync')
    parser.add_argument('src', help='where are the photos you want to copy')
    parser.add_argument('dest', help='where you want to copy your photos')
    parser.add_argument('-d', '--db', default=get_db_path_default(),
                        help='the location of the file that contains information about already transferred photos')
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    return parser


def main():
    parser = create_arg_parser()
    args = parser.parse_args()

    if args.verbose:
        LOGGER.setLevel(logging.INFO)

    db_path = args.db
    LOGGER.info('db location: %s', db_path)
    if not os.path.exists(db_path):
        init_db_file(db_path)

    src_path = Path(args.src).resolve()
    dest_path = Path(args.dest).resolve()

    db = load_db(db_path)
    synchronize(src_path, dest_path, db)
    save_db(args.db, db)


if __name__ == '__main__':
    main()
