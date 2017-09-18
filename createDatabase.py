import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Current( Base ):
    __tablename__ = 'current'
    id = Column( Integer, primary_key = True )
    artist_name = Column( String(), nullable = False)
    album_name = Column( String(), nullable = False, unique = True)
    release_year = Column( String )
    length = Column( String )
    track_number = Column( Integer )
    spotify_uri = Column( String() )
    rym_link = Column( String() )
    wikipedia_link = Column( String() )
    christgau_link = Column( String() )
    reddit_link = Column( String() )
    genius_link = Column( String() )
    songmeanings_link = Column( String() )
    youtube_link = Column( String() )

class Table( Base ):
    __tablename__ = 'table'
    id = Column( Integer, primary_key = True )
    artist_name = Column( String(), nullable = False)
    album_name = Column( String(), nullable = False, unique=True)

class Reviewed( Base ):
    __tablename__ = 'reviewed'
    id = Column( Integer, primary_key = True )
    artist_name = Column( String(), nullable = False)
    album_name = Column( String(), nullable = False, unique = True)
    rating = Column( Integer, nullable = False)
    review = Column( String, nullable = False )
    date_of_review = Column( Date, nullable = False)
    release_year = Column( String )
    length = Column( String )
    track_number = Column( Integer )
    spotify_uri = Column( String() )
    rym_link = Column( String() )
    wikipedia_link = Column( String() )
    christgau_link = Column( String() )
    reddit_link = Column( String() )
    genius_link = Column( String() )
    songmeanings_link = Column( String() )
    youtube_link = Column( String() )

engine = create_engine( 'sqlite:///test.db')
Base.metadata.create_all(engine)
