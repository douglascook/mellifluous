import os
import glob
import logging

import sqlalchemy as sqla

from models import meta, Artist

DIRECTORY = '/Users/Dug/Music/iTunes/iTunes Music/'
DB_URL = 'sqlite:///music.db'

log_format = '%(asctime)s %(levelname)s:%(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)

engine = sqla.create_engine(DB_URL)
Session = sqla.orm.sessionmaker(bind=engine)


def run():
    create_db()
    artists = get_artists(DIRECTORY)
    populate_artists(artists)


def create_db():
    meta.create_all(engine)


def populate_artists(artist_names):
    artists = [Artist(name=a) for a in artist_names]
    session = Session()
    session.add_all(artists)
    session.commit()


def get_artists(directory):
    artists = [os.path.basename(d) for d in glob.glob(directory + '*')]
    logging.info('Found {} artists'.format(len(artists)))

    return artists


if __name__ == '__main__':
    run()
