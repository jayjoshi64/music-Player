from songManager import *
from PyQt4 import QtGui, QtCore

class myListItem(QtGui.QListWidgetItem):

    def __init__(self, text, obj , master = None):
        
        QtGui.QListWidgetItem.__init__(self, text, parent=master)
        self.container = obj




class myListWidget(QtGui.QListWidget):

    """ An abstract class for listwidget. 

    methods:
    ============
    1. fillList
    2. listItemCliecked
    3. longPress (context menu event)

    """

    def __init__(self, master=None):
        QtGui.QListWidget.__init__(self,master)
        
        self.itemClicked.connect(self.listItemClicked)

        self.filler = None

    def fillList(self,filler):
        """Method to fill the list with item
        """
        #print self.filler
        self.clear()
        for each in filler:
            self.addItem(myListItem(each[0],each,master=self))

    def addToQueue(self, shuffle=False, atEnd=False):
        """<abstract method>

        will add song list to the songQ object.! by simply calling the functions of the songQ
        no written desc. in the overridden methods.
        Parameters:
        ===========
        :shuffle=False:  does it have to shuffle the song or not.?
        :atEnd=False: should the songs added at the end of the songQ.?
        
        Return: None
        
        """
        return

    def listItemClicked(self):
        """<abstract method>
        When a item is clicked in the list.
        :a new list should be shown or the song should be added to the songQ and play :)
        """

        pass

    def contextMenuEvent(self,event):
        """RightClicked pressed. show a QMenu
        <not an abstract method.!>

        should show a QMenu. 
        Options:
        ===========
        Play : will add songs to SongQ in front and play()
        Play in Shuffle : will add songs to SongQ in front in shuffled manner and play()
        Add to queue : will add songs to the queue 
        Delete : will delete the song or album or artist and apropriate songs. ( confirmation should be there.! )

        """
        pass

class SongListWidget(myListWidget):

    """List Widget class for Favourite songs
    """

    def __init__(self, songmanager,master=None):
        myListWidget.__init__(self,master)
        self.songpool = songmanager.getSongs()

        self.fillList(self.songpool)

    def listItemClicked(self):
        print "Song clicked.!"


class AlbumListWidget(myListWidget):

    """List Widget calss for albums
    """

    def __init__(self,songmanager,master=None):
        myListWidget.__init__(self,master)
        
        self.albumpool = songmanager.getAlbums()
        self.fillList(self.albumpool)

class ArtistListWidget(myListWidget):

    """List widget class for artists
    """

    def __init__(self,songmanager,master=None):
        myListWidget.__init__(self,master)
        self.artistpool = songmanager.getArtists()
        self.fillList(self.artistpool)

class PlaylistWidget(myListWidget):

    """List widget class for playlists
    """
    def __init__(self,songmanager,master=None):
        myListWidget.__init__(self,master)
        self.playlistpool = songmanager.getPlaylists()
        self.fillList(self.playlistpool)




