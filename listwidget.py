#from songManager import SongManager
from PyQt4 import QtGui#, QtCore
import random
class myListItem(QtGui.QListWidgetItem):

    def __init__(self, text, obj, master=None):        
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
        QtGui.QListWidget.__init__(self, master)
        self.itemClicked.connect(self.listItemClicked)
        self.filler = None
        self.musicPlayer = master
        self.pool = None

    def fillList(self ):
        """Method to fill the list with item
        """
        self.clear()
        for each in self.pool:
            self.addItem(myListItem(each[0], self.pool[each], master=self))

    def addToQueue(self, listtoadd ,shuffle=False, atEnd=False):
        """<abstract method>

        will add song list to the songQ object.! by simply calling the functions of the songQ
        no written desc. in the overridden methods.
        Parameters:
        ===========
        :shuffle=False:  does it have to shuffle the song or not.?
        :atEnd=False: should the songs added at the end of the songQ.?
        Return: None
        """
        
        if shuffle:
            random.shuffle(listtoadd)
            


        if atEnd:
            self.musicPlayer.songQ.addEnd(listtoadd)
        else:
            self.musicPlayer.songQ.addStart(listtoadd)

    def listItemClicked(self, item):
        """<abstract method>
        When a item is clicked in the list.
        :a new list should be shown or the song should be added to the songQ and play :)
        """

        pass

    def contextMenuEvent(self, event):
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

    def __init__(self, pool, master=None):
        myListWidget.__init__(self, master)
        self.pool = pool
        
        self.fillList()

    def listItemClicked(self, item):

        self.addToQueue([item.container],atEnd=False,shuffle=False)
        self.musicPlayer.PlayPause()
        
    
class AlbumListWidget(myListWidget):

    """List Widget calss for albums
    """

    def __init__(self, pool, master=None):
        myListWidget.__init__(self, master)
        self.pool = pool
        self.fillList()

    def listItemClicked(self, item):

        # add Album list to SongQ method
        # CHANGE THIS to album click method.!!!!!

        self.musicPlayer.songslist.pool = item.container.songlist
        self.musicPlayer.songslist.fillList()
        self.hide()
        self.musicPlayer.songslist.show()

    def contextMenuEvent(self,item):
        songlist = []
        print str(item.container)
        for eachKey in item.container.songlist:

            songlist.append(item.container.songlist[eachKey])

        print songlist
        self.addToQueue(songlist,atEnd=False,shuffle=False)
        self.musicPlayer.PlayPause()


class ArtistListWidget(myListWidget):

    """List widget class for artists
    """

    def __init__(self, pool, master=None):
        myListWidget.__init__(self, master)
        self.pool = pool
        self.fillList()

class PlaylistWidget(myListWidget):

    """List widget class for playlists
    """
    def __init__(self, pool, master=None):
        myListWidget.__init__(self, master)
        self.pool = pool
        self.fillList()

    
    def listItemClicked(self, item):

        # add playlist to SongQ method
        # CHANGE THIS to album click method.!!!!!

        self.musicPlayer.songslist.pool = item.container.songlist
        self.musicPlayer.songslist.fillList()
        self.hide()
        self.musicPlayer.songslist.show()



