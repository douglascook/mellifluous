import discogs_client
import auth

from models import meta, Artist
from db_setup import Session

discogs = discogs_client.Client('MetadataLibrarian/0.1', user_token=auth.TOKEN)
session = Session()
artists = session.query(Artist)

results = discogs.search('sporto kantes - 3 at last', type='title')
release = results[0]
