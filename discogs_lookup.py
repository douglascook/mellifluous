import logging
import re

import discogs_client
import auth

from models import meta, Artist
from db_setup import Session


logger = logging.getLogger('logalog')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

discogs = discogs_client.Client('MetadataLibrarian/0.1', user_token=auth.TOKEN)
session = Session()


def boom():
    artists = session.query(Artist)

    for artist in artists:
        for release in artist.releases:
            logger.info('Searching for {} - {}'.format(artist.name, release.title))

            hit = search(artist.name, release.title)
            if hit:
                if normalise(hit.artists[0].name) == normalise(artist.name):
                    logger.debug('Found one!')
                    update_artist(artist, hit.artists[0])
                    update_release(release, hit)
                    import ipdb; ipdb.set_trace()
                    continue


def search(artist, release):
    """Search for a release by a particular artists.

    Querying by title should hopefully return more relevant results.
    """
    search_string = '{} - {}'.format(artist, release)
    results = discogs.search(search_string, type='title')

    return select_main_release(results)


def select_main_release(results):
    """Retrieve the first main release from results."""
    for hit in results:
        if isinstance(hit, discogs_client.models.Release):
            if hit.master and hit.master.main_release:
                return hit.master.main_release
            else:
                return hit

        if isinstance(hit, discogs_client.models.Master):
            if hit.main_release:
                return hit.main_release
            else:
                logger.info('Master has no main release :(')

    logger.debug('No release found.')
    return None


def normalise(string):
    """Normalise a string for comparison with search results."""
    string = string.lower()
    string = re.sub('\W+', '', string).lower()

    return string


def update_artist(db_artist, artist):
    """Update artist details in database with retrieved data."""
    logger.info('Writing details for {} to db'.format(db_artist.name))

    db_artist.discogs_id = artist.id
    db_artist.discogs_name = artist.name
    db_artist.description = artist.profile

    urls = artist.urls
    if urls:
        db_artist.urls = ','.join(urls)

    aliases = ['{}:{}'.format(a.id, a.name) for a in artist.aliases]
    if aliases:
        db_artist.alises = ','.join(aliases)

    members = ['{}:{}'.format(a.id, a.name) for a in artist.members]
    if members:
        db_artist.members = ','.join(members)

    session.add(db_artist)
    session.commit()


def update_release(db_release, release):
    pass


if __name__ == '__main__':
    boom()
