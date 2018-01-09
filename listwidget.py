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

    def fillList(self):
        """Method to fill the list with item
        """
        print self.filler
        for each in self.filler:
            self.addItem(myListItem(each[0],each,master=self))


    def listItemClicked(self):
        """When a item is clicked in the list.
        """

        pass

    def contextMenuEvent(event):
        """RightClicked pressed. show a QMenu 
        """
        pass

class SongListWidget(myListWidget):

    """List Widget class for Favourite songs
    """

    def __init__(self, songmanager,master=None):
        myListWidget.__init__(self,master)
        self.filler = songmanager.getSongs()

        self.fillList()

class AlbumListWidget(myListWidget):

    """List Widget calss for albums
    """

    def __init__(self,songmanager,master=None):
        myListWidget.__init__(self,master)
        self.filler = songmanager.getAlbums()
        self.fillList()

class ArtistListWidget(myListWidget):

    """List widget class for artists
    """

    def __init__(self,songmanager,master=None):
        myListWidget.__init__(self,master)
        self.filler = songmanager.getArtists()
        self.fillList()

class PlaylistWidget(myListWidget):

    """List widget class for playlists
    """
    def __init__(self,songmanager,master=None):
        myListWidget.__init__(self,master)
        self.filler = songmanager.getPlaylists()
        self.fillList()




