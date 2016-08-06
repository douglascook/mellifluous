import re

import discogs_client

import auth
from log import logger
from models import meta, Artist
from db_setup import Session


discogs = discogs_client.Client('MetadataLibrarian/0.1', user_token=auth.DISCOGS_TOKEN)
session = Session()


def boom(refresh_all=False):
    artists = session.query(Artist)
    if not refresh_all:
        artists = artists.filter(Artist.searched_for.is_(False))

    for artist in artists:
        update_metadata(artist)
        artist.searched_for = True
        session.commit()


def update_metadata(artist):
    """Search for a matching artist in discogs and update the record."""
    logger.info('Updating {}'.format(artist.name))

    for release in artist.releases:
        hit = search(artist.name, release.title)
        if hit:
            if normalise(hit.artists[0].name) == normalise(artist.name):
                logger.debug('Found one!')
                update_artist(artist, hit.artists[0])
                update_release(release, hit)
                break


def search(artist, release):
    """Search for a release by a particular artists.

    Querying by title should hopefully return more relevant results.
    """
    search_string = '{} - {}'.format(artist, release)
    logger.info('Searching for {}'.format(search_string))
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
