from tkinter import *
from tkinter import ttk
import tkinter as tk
import re
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from createDatabase import Base, Current, Table, Reviewed
import datetime
import tkinter.scrolledtext as ScrolledText
import random
import os
import webbrowser
import spotipy

engine = create_engine( 'sqlite:///music.db')
Base.metadata.bind = engine
DBSession = sessionmaker( bind = engine)
session = DBSession()

class GUI_Interface:
    def __init__( self, master ):
        self.master = master
        self.createNotebook()
        self.createTableInput()
        self.createReviewInput()

    def createNotebook(self):
        nb = ttk.Notebook( self.master )
        
        self.page1 = Frame(nb)
        self.page1.configure(width=600, height=180) 
        self.page2 = Frame(nb )
        self.page2.configure(width=600, height=400)
        nb.add( self.page1, text = "Input album")
        nb.add( self.page2, text = "Review album")
        nb.pack( expand=1, fill="both")

    def createTableInput( self ):
        self.tableFrame1 = tk.Frame( self.page1 )
        self.tableFrame1.pack()

        self.inputArtist = StringVar()
        self.inputAlbum = StringVar()

        self.artistLabel = tk.Label( self.tableFrame1, text="Artist name:")
        self.albumLabel = tk.Label( self.tableFrame1, text="Album name:")
        self.artistEntry = tk.Entry( self.tableFrame1, width=25, textvariable=self.inputArtist )    
        self.albumEntry = tk.Entry( self.tableFrame1, width=25, textvariable=self.inputAlbum )
        self.submitButton = tk.Button( self.tableFrame1, text="Submit", command=self.createTableEntry)
        self.messageLabel = tk.Label( self.tableFrame1, text="" )
        
        self.artistLabel.grid( row=0, column=0 )
        self.albumLabel.grid( row=0, column=1 )
        self.artistEntry.grid( row=1, column=0 )
        self.albumEntry.grid( row=1, column=1 )
        self.submitButton.grid( row=2, column=0 )
        self.messageLabel.grid( row=2, column=1)

    def createReviewInput( self ):
        self.tableFrame2 = tk.Frame( self.page2)
        self.tableFrame2.pack()

        self.review = StringVar()
        self.rating = StringVar()
       
        self.reviewsLabel = tk.Label( self.tableFrame2, text="Albums reviewed")
        self.numReviews = tk.Label( self.tableFrame2, text="")
        self.tableLabel = tk.Label( self.tableFrame2, text="Albums to listen:")
        self.albumCount = tk.Label( self.tableFrame2, text="test")
        self.albumColumnLabel = tk.Label( self.tableFrame2, text='Current album:')
        self.chosenAlbumLabel = tk.Label( self.tableFrame2, text="None")
        self.playButton = tk.Button( self.tableFrame2, text="Play", command=self.playSpotify)
        self.newAlbumButton = tk.Button( self.tableFrame2, text="New Album", command=self.chooseAlbum)
        self.wikiButton = tk.Button( self.tableFrame2, text="Wiki", command= lambda: self.openPage(0))
        self.lyricsButton = tk.Button( self.tableFrame2, text="Lyrics", command= lambda: self.openPage(1))
        self.rymButton = tk.Button( self.tableFrame2, text="RYM", command= lambda: self.openPage( 2 ))
        self.ratingLabel = tk.Label( self.tableFrame2, text="Rating:")
        self.ratingEntry = tk.Entry( self.tableFrame2, width=8, textvariable=self.rating )
        self.reviewField = ScrolledText.ScrolledText(self.tableFrame2, height=8, width=120, font = ('Helvetica',12), borderwidth=3, relief=SUNKEN)
        self.reviewSubmitButton = tk.Button( self.tableFrame2, text="Submit", command=self.reviewAlbum)
        self.messageLabel2 = tk.Label( self.tableFrame2, text="")

        self.reviewsLabel.grid( row=0, column=0)
        self.numReviews.grid( row=0, column=1)
        self.newAlbumButton.grid( row=0, rowspan=2, column=2)
        self.tableLabel.grid( row=1, column=0)
        self.albumCount.grid( row=1, column=1)
        self.albumColumnLabel.grid( row=2, column=0, pady=(25,2))
        self.chosenAlbumLabel.grid( row=2, column=1, pady=(25,2))
        self.playButton.grid( row=2, column=2, pady=( 25, 2))
        self.wikiButton.grid( row=3, column=0)
        self.lyricsButton.grid( row=3, column=1)
        self.rymButton.grid( row=3, column=2)
        self.reviewField.grid( row=4, columnspan=3)
        self.ratingLabel.grid( row=5, column=0)
        self.ratingEntry.grid( row=5, column=1)
        self.reviewSubmitButton.grid( row=5, column=2)
        self.messageLabel2.grid( row=6, columnspan=3)
        self.displayCurrent()
        self.displayTableCount()
        self.displayReviewCount()

    def createTableEntry( self ):
        inputArtist = self.inputArtist.get()
        inputAlbum = self.inputAlbum.get()
       
        if not inputArtist or not inputAlbum:
            self.message( "Invalid entry!", self.messageLabel)
            return

        if session.query(Table).first() is not None and session.query(Table).filter_by(album_name=inputAlbum).scalar() is not None:
            self.message(inputAlbum + " is already on table!", self.messageLabel)
        elif session.query(Reviewed).first() is not None and session.query(Reviewed).filter_by(album_name=inputAlbum).scalar() is not None:
            self.message(inputAlbum + " has already been reviewed!", self.messageLabel)
        elif session.query(Current).first() is not None and session.query(Current).filter_by(album_name=inputAlbum).scalar() is not None:
            self.message(inputAlbum + " is currently up for review!", self.messageLabel)
        else:
            table = Table( artist_name=inputArtist, album_name=inputAlbum )
            session.add( table )
            session.commit()
            self.clearFieldsPage1()
            self.message( inputAlbum + " is now on the Table.", self.messageLabel)
            self.displayTableCount()
    
    def chooseAlbum( self ): 
        if session.query( Table ).first() is None:
            self.message( "Nothing on the Table!", self.messageLabel2)
        elif session.query( Current ).first() is not None:
            self.message("Must review current album first!", self.messageLabel2)
            self.displayCurrent()
        else:
            # authenticate spotify
            os.system( "sh ./auth.sh > token.txt")
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
            with open('token.txt', 'r') as myfile:
                token=myfile.read().replace('\n', '')

            spotify = spotipy.Spotify(auth=token)

            #get random album from table
            rand = random.randrange(0, session.query(Table).count())
            randAlbum = session.query(Table)[rand]  
            
            #get spotify URI
            name = randAlbum.album_name + " " + randAlbum.artist_name
            results = spotify.search(q='album:' + name, type='album')
            items = results['albums']['items']
            if len(items) > 0:
                spAlbum = items[0]
                listenLink = spAlbum['uri']
            else:
                listenLink = self.getFirstURL( "youtube full album " + name)
                self.message( "Failed to find album on spotify!", self.messageLabel2)
            #get links
            wiki = self.getFirstURL("wikipedia " + name)
            lyrics = self.getFirstURL( "genius " + name)
            rym = self.getFirstURL( "rate your music " + name)

            #create row object
            newCurrent = Current( 
                    artist_name=randAlbum.artist_name, 
                    album_name=randAlbum.album_name, 
                    spotify_uri = listenLink,
                    wikipedia_link = wiki,
                    songmeanings_link = lyrics,
                    rym_link = rym )

            #commit to database
            session.add( newCurrent )
            session.commit()
            session.delete(session.query(Table).get(randAlbum.id))
            session.commit()
            self.displayCurrent()
            self.displayTableCount()
            os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

    def displayCurrent( self):
        if( session.query(Current).first() is not None):
            self.current = session.query(Current).first()
            name = self.current.artist_name + " - " + self.current.album_name 
            self.chosenAlbumLabel.configure( text=name)
        else:
            self.chosenAlbumLabel.configure( text="None") 

    def displayTableCount( self ):
        self.albumCount.configure( text=str(session.query(Table).count()))
    
    def displayReviewCount( self ):
        self.numReviews.configure( text=str( session.query(Reviewed).count()))

    def reviewAlbum( self ):
        if session.query( Current ).first() is None:
            self.message( "No album to review!", self.messageLabel2)
        else:
            review=self.reviewField.get(1.0, END)
            rating=self.rating.get()
            try:
                ratingInt = int(rating)
            except:
                self.message( "Invalid rating", self.messageLabel2)
                return
            if ratingInt < 1 or ratingInt > 10:
                self.message( "Invalid rating", self.messageLabel2)
                return
            newReview = Reviewed( artist_name=self.current.artist_name, album_name=self.current.album_name, review=review, rating=rating, date_of_review=datetime.datetime.now().date() )
            session.add( newReview )
            session.commit()

            session.delete(self.current)
            session.commit()

            self.chosenAlbumLabel.configure(text="None")
            self.clearFieldsPage2()
            self.message( self.current.album_name+" reviewed.", self.messageLabel2)
            self.displayTableCount()
            self.displayReviewCount()
        
    def message( self, text, label ):
        label.config( text="")
        label.config( text=text)

    def clearFieldsPage1(self):
        self.artistEntry.delete( 0, 'end')
        self.albumEntry.delete( 0, 'end')
    
    def clearFieldsPage2(self):
        self.reviewField.delete('1.0',END)
        self.ratingEntry.delete(0,'end')

    def playSpotify( self ):
        link = session.query( Current ).one().spotify_uri
        if "youtube" in link:
            self.openChrome( link )
        else:
            os.system( "spotify play " + session.query( Current ).one().spotify_uri )
        self.message( "Now playing album.", self.messageLabel2)

    def openPage( self, index):
        if session.query( Current ).first() is None:
            self.message( "No album selected!", self.messageLabel2)
        else:
            current = session.query(Current).one()
            url = ""
            if index == 0 and current.wikipedia_link:
                url = current.wikipedia_link
            elif index == 1 and current.songmeanings_link:
                url = current.songmeanings_link
            elif index == 2 and current.rym_link:
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
        soup = BeautifulSoup(page.content, "lxml")
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
