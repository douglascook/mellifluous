import os
import glob
import logging

import sqlalchemy as sqla

from models import meta, Artist, Release


DIRECTORY = '/Users/Dug/Music/iTunes/iTunes Music/'
DB_URL = 'sqlite:///music.sqlite'

log_format = '%(asctime)s %(levelname)s:%(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)

engine = sqla.create_engine(DB_URL)
Session = sqla.orm.sessionmaker(bind=engine)


def run():
    create_db()
    record_artists_and_releases()


def create_db():
    meta.create_all(engine)


def record_artists_and_releases():
    """Create skeleton records in artists and releases tables from given
    directory.

    Assume that directory structure is artist/albums/tracks a la itunes library.
    """
    total_artists = 0
    total_releases = 0
    session = Session()

    artists = []
    for artist_dir in glob.glob(DIRECTORY + '*'):
        artist = Artist(name=os.path.basename(artist_dir))
        total_artists += 1

        for release_dir in glob.glob(artist_dir + '/*'):
            release = Release(title=os.path.basename(release_dir))
            artist.releases.append(release)
            total_releases += 1

        artists.append(artist)

    logging.info('Adding {} artists with {} releases'.format(
        total_artists, total_releases))

    session.add_all(artists)
    session.commit()


if __name__ == '__main__':
    run()
