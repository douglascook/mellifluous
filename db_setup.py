import os
import glob

import sqlalchemy as sqla

from models import meta

DIRECTORY = '/Users/Dug/Music/iTunes/iTunes Music/'
DB_URL = 'sqlite:///music.db'
ENGINE = sqla.create_engine(DB_URL, echo=True)


def create_db():
    meta.create_all(ENGINE)


def get_artists(directory):
    artists = [os.path.basename(f) for f in glob.glob(directory + '*')]
    return artists


if __name__ == '__main__':
    create_db()
