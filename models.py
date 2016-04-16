from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()
meta = Base.metadata


# tables for many to many relationships with releases
release_genre_association = Table(
    'release_genre', meta,
    Column('release_id', Integer, ForeignKey('releases.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)


release_style_association = Table(
    'release_style', meta,
    Column('release_id', Integer, ForeignKey('releases.id')),
    Column('style_id', Integer, ForeignKey('styles.id'))
)


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)

    discogs_id = Column(Integer, unique=True)
    discogs_name = Column(String)
    description = Column(String)
    urls = Column(String)
    aliases = Column(String)
    members = Column(String)

    releases = relationship('Release', back_populates='artist')

    def __repr__(self):
        return self.name


class Release(Base):
    __tablename__ = 'releases'

    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String)
    artist_id = Column(Integer, ForeignKey('artists.id'))
    # TODO add label relationship

    discogs_id = Column(Integer, unique=True)
    discogs_title = Column(String)
    styles = Column(String)
    year = Column(Integer)
    genres = Column(String)
    country = Column(String)
    urls = Column(String)
    artists = Column(String)
    labels = Column(String)

    artist = relationship('Artist', back_populates='releases')
    tracks = relationship('Track', back_populates='release')
    genres = relationship('Genre', secondary=release_genre_association)
    styles = relationship('Style', secondary=release_style_association)

    def __repr__(self):
        return self.title


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True, unique=True)
    release_id = Column(Integer, ForeignKey('releases.id'))

    title = Column(String)
    duration = Column(String)
    artists = Column(String)

    release = relationship('Release', back_populates='tracks')

    def __repr__(self):
        return self.title


class Label(Base):
    __tablename__ = 'labels'

    id = Column(Integer, primary_key=True, unique=True)

    discogs_id = Column(Integer, unique=True)
    name = Column(String)
    description = Column(String)
    urls = Column(String)

    def __repr__(self):
        return self.name


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, unique=True)
    genre = Column(String)

    def __repr__(self):
        return self.genre


class Style(Base):
    __tablename__ = 'styles'

    id = Column(Integer, primary_key=True, unique=True)
    style = Column(String)

    def __repr__(self):
        return self.style
