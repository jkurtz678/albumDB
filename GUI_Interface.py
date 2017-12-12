from tkinter import *
from tkinter import ttk
import tkinter as tk
import re
import requests
import bs4 as bs
import urllib.request
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from createDatabase import Base, Current, Table, Reviewed
import datetime
import tkinter.scrolledtext as ScrolledText
import random
import os
import webbrowser
import spotipy

#bcolor= "#9FBED6"
bcolor= "#ffffff"
color= ""
#engine = create_engine( 'sqlite:///music.db')
engine = create_engine( 'sqlite:////Users/jacksonkurtz/Documents/Code/Personal/PopMusicDB/test.db')
Base.metadata.bind = engine
DBSession = sessionmaker( bind = engine)
session = DBSession()

class GUI_Interface:
    def __init__( self, master ):
        self.master = master
        self.createNotebook()
        self.createTableInput()
        self.createInfoWindow()
        self.createReviewInput()

    def createNotebook(self):
        nb = ttk.Notebook( self.master )
        
        self.page1 = Frame(nb, bg=bcolor )
        self.page1.configure(width=600, height=180) 
        self.page2 = Frame(nb, bg=bcolor )
        self.page2.configure(width=600, height=400)
        self.page3 = Frame(nb, bg=bcolor)
        self.page3.configure(width=600, height=400)
        nb.add( self.page1, text = "Input")
        nb.add( self.page2, text = "Current")
        nb.add( self.page3, text = "Review")
        nb.pack( expand=1, fill="both")

    def createTableInput( self ):
        self.tableFrame1 = tk.Frame( self.page1, bg=bcolor, height=350 )
        self.infoFrame1 = tk.Frame( self.page1, height=50)
        self.infoFrame1.pack()
        self.tableFrame1.pack()
        
        #variables
        self.inputArtist = StringVar()
        self.inputAlbum = StringVar()
        self.genre = StringVar() 
        self.genreList = {"Pop", "New", "Classical", "Jazz"}
        self.genre.set("Pop")

        #infoFrame
        self.countLabel = tk.Label( self.infoFrame1, text="Albums on table")
        self.newLabel = tk.Label( self.infoFrame1, text="New:")
        self.popLabel = tk.Label( self.infoFrame1, text="Pop:")
        self.classicalLabel = tk.Label( self.infoFrame1, text="Classical:")
        self.jazzLabel = tk.Label( self.infoFrame1, text="Jazz:")
        self.totalLabel = tk.Label( self.infoFrame1, text="Total:")
        self.newCountLabel = tk.Label( self.infoFrame1, text="")
        self.popCountLabel = tk.Label( self.infoFrame1, text="")
        self.classicalCountLabel = tk.Label( self.infoFrame1, text="")
        self.jazzCountLabel = tk.Label( self.infoFrame1, text="")
        self.totalCountLabel = tk.Label( self.infoFrame1, text="")

        self.countLabel.grid( row=0, columnspan=5)
        self.newLabel.grid( row=1, column=0, padx=(15,15))
        self.popLabel.grid( row=1, column=1, padx=(15,15))
        self.classicalLabel.grid( row=1, column=2, padx=(15,15))
        self.jazzLabel.grid( row=1, column=3, padx=(15,15))
        self.totalLabel.grid( row=1, column=4, padx=(15,15))
        self.newCountLabel.grid( row=2, column=0)
        self.popCountLabel.grid( row=2, column=1)
        self.classicalCountLabel.grid( row=2, column=2)
        self.jazzCountLabel.grid( row=2, column=3)
        self.totalCountLabel.grid(row=2, column=4)
        
        #tableFrame
        self.artistLabel = tk.Label( self.tableFrame1, text="Artist name:")
        self.albumLabel = tk.Label( self.tableFrame1, text="Album name:")
        self.artistEntry = tk.Entry( self.tableFrame1, width=25, textvariable=self.inputArtist )    
        self.albumEntry = tk.Entry( self.tableFrame1, width=25, textvariable=self.inputAlbum )
        self.genreLabel = tk.Label( self.tableFrame1, text="Genre Category:")
        self.genreMenu = tk.OptionMenu( self.tableFrame1, self.genre, *self.genreList )
        self.genreMenu.configure(width=10)
        self.submitButton = tk.Button( self.tableFrame1, text="Submit", command=self.createTableEntry)
        self.messageLabel = tk.Label( self.tableFrame1, text="" )
        
        self.artistLabel.grid( row=0, column=0, pady=(35,5) )
        self.albumLabel.grid( row=0, column=1, pady=(35,5))
        self.artistEntry.grid( row=1, column=0, pady=(5,15), padx=(10,10) )
        self.albumEntry.grid( row=1, column=1, pady=(5,15), padx=(10,10) )
        self.genreLabel.grid( row=2, column=0 )
        self.genreMenu.grid( row=3, column=0 )
        self.submitButton.grid( row=2, rowspan=2, column=1, pady=(20,10) )
        self.messageLabel.grid( row=4, column=0, columnspan=2, pady=(20,10) )

        self.displayTableCount()

    def createInfoWindow( self ):
        self.tableFrame2 = tk.Frame( self.page2, bg=bcolor)
        self.tableFrame2.pack()
        

        #category column
        self.categoryColumnLabel = tk.Label( self.tableFrame2, text="Category")
        self.newRowLabel = tk.Label( self.tableFrame2, text="New")        
        self.popRowLabel = tk.Label( self.tableFrame2, text="Pop")
        self.classicalRowLabel = tk.Label( self.tableFrame2, text="Classical")
        self.jazzRowLabel = tk.Label( self.tableFrame2, text="Jazz")

        self.categoryColumnLabel.grid( row=0, column=0, pady=(20,20))
        self.newRowLabel.grid( row=1, column=0, pady=(20,20))
        self.popRowLabel.grid( row=2, column=0, pady=(20,20))
        self.classicalRowLabel.grid( row=3, column=0, pady=(20,20))
        self.jazzRowLabel.grid( row=4, column=0, pady=(20,20))

        #artist column
        self.artistColumnLabel = tk.Label( self.tableFrame2, text="Artist")
        self.newArtistLabel = tk.Label( self.tableFrame2, text="")
        self.popArtistLabel = tk.Label( self.tableFrame2, text="")
        self.classicalArtistLabel = tk.Label( self.tableFrame2, text="")
        self.jazzArtistLabel = tk.Label( self.tableFrame2, text="")
        
        self.artistColumnLabel.grid( row=0, column=1)
        self.newArtistLabel.grid( row=1, column=1)
        self.popArtistLabel.grid( row=2, column=1)
        self.classicalArtistLabel.grid( row=3, column=1)
        self.jazzArtistLabel.grid( row=4, column=1)

        #album column
        self.albumColumnLabel = tk.Label( self.tableFrame2, text="Album")
        self.newAlbumLabel = tk.Label( self.tableFrame2, text="")
        self.popAlbumLabel = tk.Label( self.tableFrame2, text="")
        self.classicalAlbumLabel = tk.Label( self.tableFrame2, text="")
        self.jazzAlbumLabel = tk.Label( self.tableFrame2, text="")

        self.albumColumnLabel.grid( row=0, column=2)
        self.newAlbumLabel.grid( row=1, column=2)
        self.popAlbumLabel.grid( row=2, column=2)
        self.classicalAlbumLabel.grid( row=3, column=2)
        self.jazzAlbumLabel.grid( row=4, column=2)

        #date column
        self.dateColumnLabel = tk.Label( self.tableFrame2, text="Date")
        self.newDateLabel = tk.Label( self.tableFrame2, text="")
        self.popDateLabel = tk.Label( self.tableFrame2, text="")
        self.classicalDateLabel = tk.Label( self.tableFrame2, text="")
        self.jazzDateLabel = tk.Label( self.tableFrame2, text="")
        
        self.dateColumnLabel.grid( row=0, column=3)
        self.newDateLabel.grid( row=1, column=3)
        self.popDateLabel.grid( row=2, column=3)
        self.classicalDateLabel.grid( row=3, column=3)
        self.jazzDateLabel.grid( row=4, column=3)

        #length column
        self.lengthColumnLabel = tk.Label( self.tableFrame2, text="Length")
        self.newLengthLabel = tk.Label( self.tableFrame2, text="")
        self.popLengthLabel = tk.Label( self.tableFrame2, text="")
        self.classicalLengthLabel = tk.Label( self.tableFrame2, text="")
        self.jazzLengthLabel = tk.Label( self.tableFrame2, text="")
        
        self.lengthColumnLabel.grid( row=0, column=4)
        self.newLengthLabel.grid( row=1, column=4)
        self.popLengthLabel.grid( row=2, column=4)
        self.classicalLengthLabel.grid( row=3, column=4)
        self.jazzLengthLabel.grid( row=4, column=4)

        #wiki column
        self.wikiColumnLabel = tk.Label( self.tableFrame2, text="Wiki")
        self.newWikiButton = tk.Button( self.tableFrame2, text="Wiki", command= lambda: self.openPage("New",0) )
        self.popWikiButton = tk.Button( self.tableFrame2, text="Wiki", command= lambda: self.openPage("Pop",0) )
        self.classicalWikiButton = tk.Button( self.tableFrame2, text="Wiki", command= lambda: self.openPage("Classical",0) )
        self.jazzWikiButton = tk.Button( self.tableFrame2, text="Wiki", command= lambda: self.openPage("Jazz",0) )

        self.wikiColumnLabel.grid( row=0, column=5)
        self.newWikiButton.grid( row=1, column=5)
        self.popWikiButton.grid( row=2, column=5)
        self.classicalWikiButton.grid( row=3, column=5)
        self.jazzWikiButton.grid( row=4, column=5)

        #rym column
        self.rymColumnLabel = tk.Label( self.tableFrame2, text="RYM")
        self.newRymButton = tk.Button( self.tableFrame2, text="RYM", command= lambda: self.openPage("New",1) )
        self.popRymButton = tk.Button( self.tableFrame2, text="RYM", command= lambda: self.openPage("Pop",1) )
        self.classicalRymButton = tk.Button( self.tableFrame2, text="RYM", command= lambda: self.openPage("Classical",1) )
        self.jazzRymButton = tk.Button( self.tableFrame2, text="RYM", command= lambda: self.openPage("Jazz",1) )
        
        self.rymColumnLabel.grid( row=0, column=6)
        self.newRymButton.grid( row=1, column=6)
        self.popRymButton.grid( row=2, column=6)
        self.classicalRymButton.grid( row=3, column=6)
        self.jazzRymButton.grid( row=4, column=6)

        #new album column
        self.newColumnLabel = tk.Label( self.tableFrame2, text="New Album")
        self.newNewButton = tk.Button( self.tableFrame2, text="New", command= lambda: self.chooseAlbum("New") )
        self.popNewButton = tk.Button( self.tableFrame2, text="New", command= lambda: self.chooseAlbum("Pop") )
        self.classicalNewButton = tk.Button( self.tableFrame2, text="New", command= lambda: self.chooseAlbum("Classical") )
        self.jazzNewButton = tk.Button( self.tableFrame2, text="New", command= lambda: self.chooseAlbum("Jazz") )
        
        self.newColumnLabel.grid( row=0, column=7)
        self.newNewButton.grid( row=1, column=7)
        self.popNewButton.grid( row=2, column=7)
        self.classicalNewButton.grid( row=3, column=7)
        self.jazzNewButton.grid( row=4, column=7)
 
        self.messageLabel2 = tk.Label( self.tableFrame2, text="")
        self.messageLabel2.grid( row=7, columnspan = 8 )
        self.displayCurrent()
        #self.displayTableCount()
        #self.displayReviewCount()

    def createReviewInput( self ):
        self.tableFrame3 = tk.Frame( self.page3, bg=bcolor)
        self.tableFrame3.pack()
        
        self.review = StringVar()
        self.rating = StringVar()
        self.keyTracks = StringVar()
        self.albumChoice = StringVar()
        self.albumChoice.set("Pop") 

        self.totalReviewedLabel = tk.Label( self.tableFrame3, text="Total reviewed:")
        self.totalReviewedNumber = tk.Label( self.tableFrame3, text="test")
        self.reviewMenuLabel = tk.Label( self.tableFrame3, text="Album review category:")
        self.albumGenreMenu = tk.OptionMenu( self.tableFrame3, self.albumChoice, *self.genreList, command=self.displayReviewAlbum )
        self.albumGenreMenu.configure( width=10 )
        self.chosenAlbumLabel2 = tk.Label( self.tableFrame3, text="Current album:")
        self.chosenAlbum2 = tk.Label( self.tableFrame3, text="placeholder")
        self.ratingLabel = tk.Label( self.tableFrame3, text="Rating:")
        self.ratingEntry = tk.Entry( self.tableFrame3, width=8, textvariable=self.rating )
        self.reviewLabel = tk.Label( self.tableFrame3, text="Review:")
        self.reviewField = ScrolledText.ScrolledText(self.tableFrame3, height=8, width=120, font = ('Helvetica',12), borderwidth=3, relief=SUNKEN)
        self.keyTracksLabel = tk.Label( self.tableFrame3, text="Key tracks")
        self.keyTracksEntry = tk.Entry( self.tableFrame3, width=37, textvariable=self.keyTracks )
        self.reviewSubmitButton = tk.Button( self.tableFrame3, text="Submit", width=8, command=self.reviewAlbum)
        self.messageLabel3 = tk.Label( self.tableFrame3, text="")
        
        self.totalReviewedLabel.grid( row=0, column=0, columnspan=2, pady=(10,30))
        self.totalReviewedNumber.grid( row=0, column=1, columnspan=2, pady=(10,30))
        self.reviewMenuLabel.grid( row = 1, column=0, columnspan=2 )
        self.albumGenreMenu.grid( row=2,column=0, columnspan=2, pady=(0,15))
        self.chosenAlbumLabel2.grid( row=1, column=1, columnspan=2 )
        self.chosenAlbum2.grid( row=2, column=1, columnspan=2, pady=(0,15) )
        self.reviewLabel.grid( row=3, column=0, columnspan=2)
        self.reviewField.grid( row=4, columnspan=3)
        self.keyTracksLabel.grid( row=5, column=0, pady=(8,8))
        self.keyTracksEntry.grid( row=5, column=1, columnspan=2, pady=(8,8))
        self.ratingLabel.grid( row=6, column=0)
        self.ratingEntry.grid( row=6, column=1)
        self.reviewSubmitButton.grid( row=6, column=2)
        self.messageLabel3.grid( row=7, columnspan=3, pady=(14,4)) 
        #self.displayCurrent(self.albumChoice)
        self.displayReviewCount( )
        self.displayReviewAlbum("")

    def createTableEntry( self ):
        inputArtist = self.inputArtist.get()
        inputAlbum = self.inputAlbum.get()
        genre = self.genre.get()

        if not inputArtist or not inputAlbum:
            self.message( "Invalid entry!", self.messageLabel)
            return

        if session.query(Table).first() is not None and session.query(Table).filter_by(album_name=inputAlbum).scalar() is not None:
            self.message("'" + inputAlbum + "' is already on table!", self.messageLabel)
        elif session.query(Reviewed).first() is not None and session.query(Reviewed).filter_by(album_name=inputAlbum).scalar() is not None:
            self.message("'" + inputAlbum + "' has already been reviewed!", self.messageLabel)
        elif session.query(Current).first() is not None and session.query(Current).filter_by(album_name=inputAlbum).scalar() is not None:
            self.message("'" + inputAlbum + "' is currently up for review!", self.messageLabel)
        else:
            table = Table( artist_name=inputArtist, album_name=inputAlbum, category=genre )
            session.add( table )
            session.commit()
            self.clearFieldsPage1()
            self.message( inputAlbum + " is now on the Table.", self.messageLabel)
            self.displayTableCount()
    
    def chooseAlbum( self, genre): 
        print( "choosing album...")
        if session.query( Table ).first() is None:
            self.message( "Nothing on the Table!", self.messageLabel2)
            return
        elif session.query( Current).filter_by( category=genre).first() is not None:
            self.message( "Must review current" + genre + "album first!", self.messageLabel2 )
            return
        elif session.query( Table ).filter_by( category=genre).first() is None:
            self.message( "No" + genre + "albums on the Table!", self.messageLabel2 )
            return
        else:
            rand = random.randrange(0, session.query(Table).filter_by( category=genre).count())
            randAlbum = session.query(Table).filter_by( category=genre)[rand]
        '''
        elif session.query( Current ).first() is not None:
            self.message("Must review current album first!", self.messageLabel2)
            self.displayCurrent()
         '''
        # authenticate spotify
        #print( "authenticate spotify...")
        #os.system( "sh ./auth.sh > token.txt")
        #os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
        #with open('token.txt', 'r') as myfile:
            #token=myfile.read().replace('\n', '')

        #spotify = spotipy.Spotify(auth=token)
        #get spotify URI
        name = randAlbum.album_name + " " + randAlbum.artist_name
        #results = spotify.search(q='album:' + name, type='album')
        #items = results['albums']['items']
        #if len(items) > 0:
        #    spAlbum = items[0]
        #    listenLink = spAlbum['uri']
        #else:
        #    listenLink = self.getFirstURL( "youtube full album " + name)
        #    self.message( "Failed to find album on spotify!", self.messageLabel2)

        listenLink = ""
        #get links
        print( "getting links...")
        wiki = self.getFirstURL("wikipedia " + name)
        genius = self.getFirstURL( "genius " + name)
        songmeanings = self.getFirstURL( "songmeanings " + name)
        christgau = self.getFirstURL( "robert christgau " + randAlbum.artist_name)
        reddit = self.getFirstURL( "reddit " + name)
        rym = self.getFirstURL( "rate your music " + name)

        #get info
        length = ""
        releaseDate = ""
        trackCount = 0
        print( "getting info...")
        try:
            sauce = urllib.request.urlopen(wiki).read() 
            soup = bs.BeautifulSoup( sauce, 'lxml')
            try:
                length = soup.find('span', class_="duration").text 
                releaseDate = soup.find('td', class_="published").text
                trackCount = None 
                if listenLink:
                    trackCount = spotify.album_tracks( listenLink )['total']
                else:
                    pass
            except:
                pass
        except:
            print( "Cant find sauce")
            pass
        print( "creating row object...")
        #create row object
        newCurrent = Current( 
                artist_name=randAlbum.artist_name, 
                album_name=randAlbum.album_name, 
                category=randAlbum.category,
                spotify_uri = listenLink,
                length = length,
                release_year = releaseDate,
                track_number = trackCount,
                wikipedia_link = wiki,
                songmeanings_link = songmeanings,
                genius_link = genius,
                reddit_link = reddit,
                christgau_link = christgau,
                rym_link = rym )

        #commit to database
        session.add( newCurrent )
        session.commit()
        session.delete(session.query(Table).get(randAlbum.id))
        session.commit()
        self.displayCurrent()
        self.displayTableCount()
        self.displayReviewAlbum("")
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

    def displayCurrent( self):
        #new
        if( session.query(Current).filter_by(category="New").first() is not None):
            self.currentNew = session.query(Current).filter_by(category="New").first()
            self.newAlbumLabel.configure( text=self.currentNew.artist_name)
            self.newArtistLabel.configure( text=self.currentNew.album_name)
            self.newDateLabel.configure( text=str(self.currentNew.release_year))
            self.newLengthLabel.configure( text=self.currentNew.length)
        else:
            self.newAlbumLabel.configure( text="-") 
            self.newArtistLabel.configure( text="-")
            self.newDateLabel.configure( text="-") 
            self.newLengthLabel.configure( text="-")
        #pop
        if( session.query(Current).filter_by(category="Pop").first() is not None):
            self.currentPop = session.query(Current).filter_by(category="Pop").first()
            self.popAlbumLabel.configure( text=self.currentPop.artist_name)
            self.popArtistLabel.configure( text=self.currentPop.album_name)
            self.popDateLabel.configure( text=str(self.currentPop.release_year))
            self.popLengthLabel.configure( text=self.currentPop.length)
        else:
            self.popAlbumLabel.configure( text="-") 
            self.popArtistLabel.configure( text="-")
            self.popDateLabel.configure( text="-") 
            self.popLengthLabel.configure( text="-")
        #classical
        if( session.query(Current).filter_by(category="Classical").first() is not None):
            self.currentClassical = session.query(Current).filter_by(category="Classical").first()
            self.classicalAlbumLabel.configure( text=self.currentClassical.artist_name)
            self.classicalArtistLabel.configure( text=self.currentClassical.album_name)
            self.classicalDateLabel.configure( text=str(self.currentClassical.release_year))
            self.classicalLengthLabel.configure( text=self.currentClassical.length)
        else:
            self.classicalAlbumLabel.configure( text="-") 
            self.classicalArtistLabel.configure( text="-")
            self.classicalDateLabel.configure( text="-") 
            self.classicalLengthLabel.configure( text="-")
        #jazz    
        if( session.query(Current).filter_by(category="Jazz").first() is not None):
            self.currentJazz = session.query(Current).filter_by(category="Jazz").first()
            self.jazzAlbumLabel.configure( text=self.currentJazz.artist_name)
            self.jazzArtistLabel.configure( text=self.currentJazz.album_name)
            self.jazzDateLabel.configure( text=str(self.currentJazz.release_year))
            self.jazzLengthLabel.configure( text=self.currentJazz.length)
        else:
            self.jazzAlbumLabel.configure( text="-") 
            self.jazzArtistLabel.configure( text="-")
            self.jazzDateLabel.configure( text="-") 
            self.jazzLengthLabel.configure( text="-")
        self.message( "", self.messageLabel2)

    def displayReviewAlbum( self, x ):
        #print( "test print" + self.albumChoice)
        album = session.query(Current).filter_by(category=self.albumChoice.get()).first()
        if album is not None:
            self.chosenAlbum2.configure( text=str(album.artist_name + " - " + album.album_name ))
        else:
            self.chosenAlbum2.configure( text="None")

    def displayTableCount( self ):
        #self.albumCount.configure( text=str(session.query(Table).count()))
        self.newCountLabel.configure( text=str(session.query(Table).filter_by(category="New").count()))
        self.popCountLabel.configure( text=str(session.query(Table).filter_by(category="Pop").count()))
        self.classicalCountLabel.configure( text=str(session.query(Table).filter_by(category="Classical").count()))
        self.jazzCountLabel.configure( text=str(session.query(Table).filter_by(category="Jazz").count()))
        self.totalCountLabel.configure( text=str(session.query(Table).count()))
    
    def displayReviewCount( self ):
        self.totalReviewedNumber.configure( text=str( session.query(Reviewed).count()))

    def reviewAlbum( self ):
        print( "review album method")
        genreChoice = self.albumChoice.get()
        if session.query( Current ).filter_by( category=genreChoice).first() is None:
            self.message( "No " + genreChoice + " album to review!", self.messageLabel3)
        else:
            current = session.query( Current ).filter_by( category=genreChoice ).first()
            review=self.reviewField.get(1.0, END)
            keyTracks = self.keyTracks.get()
            rating=self.rating.get()
            try:
                ratingInt = int(rating)
            except:
                self.message( "Invalid rating", self.messageLabel3)
                return
            if ratingInt < 1 or ratingInt > 10:
                self.message( "Invalid rating", self.messageLabel3)
                return
            newReview = Reviewed( 
                    artist_name=current.artist_name, 
                    album_name=current.album_name, 
                    category=current.category,
                    review=review,
                    key_tracks=keyTracks,
                    rating=rating, 
                    date_of_review=datetime.datetime.now().date(),
                    release_year=current.release_year,
                    length=current.length,
                    track_number=current.track_number,
                    spotify_uri=current.spotify_uri,
                    rym_link=current.rym_link,
                    wikipedia_link=current.wikipedia_link,
                    songmeanings_link=current.songmeanings_link,
                    youtube_link=current.youtube_link
                    )
            try:
                session.add( newReview )
                session.commit()
            except:
                self.message( "Error submitting review!", self.messageLabel3)
                return
            session.delete(current)
            session.commit()

            #self.chosenAlbum1.configure(text="None")
            #self.chosenAlbum2.configure(text="None")
            #self.releaseDate.configure( text="")
            #self.length.configure( text="")
            #self.trackCount.configure( text="")
        
            self.clearFieldsPage2()
            self.message( current.album_name + " reviewed.", self.messageLabel3)
            self.displayTableCount()
            self.displayReviewCount()
            self.displayReviewAlbum("")
            self.displayCurrent()
        
    def message( self, text, label ):
        label.config( text="")
        label.config( text=text)

    def clearFieldsPage1(self):
        self.artistEntry.delete( 0, 'end')
        self.albumEntry.delete( 0, 'end')
    
    def clearFieldsPage2(self):
        self.reviewField.delete('1.0',END)
        self.keyTracksEntry.delete( 0,'end')
        self.ratingEntry.delete(0,'end')

    def playSpotify( self ):
        link = session.query( Current ).one().spotify_uri
        if "youtube" in link:
            self.openChrome( link )
        else:
            os.system( "spotify play " + session.query( Current ).one().spotify_uri )
        self.message( "Now playing album.", self.messageLabel2)

    def openPage( self, genre, index):
        if session.query( Current ).filter_by(category=genre).first() is None:
            self.message( "No" + genre + "album chosen!", self.messageLabel2)
        else:
            current = session.query(Current).filter_by(category=genre).one()
            url = ""
            if index == 0 and current.wikipedia_link:
                url = current.wikipedia_link
            elif index == 1 and current.rym_link:
                url = current.rym_link
            else:
                self.message( "Unable to find url", self.messageLabel2)
                return
            self.openChrome( url )

    def openChrome( self, url):
        chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        webbrowser.get(chrome_path).open(url)

    def getFirstURL( self, search ):
        results = 1 
        page = requests.get("https://www.google.com/search?q={}&num={}".format(search, results))
        soup = bs.BeautifulSoup(page.content, "lxml")
        links = soup.findAll("a")
        for link in links :
            link_href = link.get('href')
            if "url?q=" in link_href and not "webcache" in link_href:
                return (link.get('href').split("?q=")[1].split("&sa=U")[0])

def main():
    root = Tk()
    app = GUI_Interface( root )
    #root.lift("-topmost", True)
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

    root.mainloop()

if __name__ == '__main__':
    main()
