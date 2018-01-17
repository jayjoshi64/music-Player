
"""
A music player working with PyQt4 and VLC.

"""
import sys
import os
import user
import vlc
from styles import *
from listwidget import *
from songManager import SongManager
from PyQt4 import QtGui, QtCore
from songQ import SongQ

class Player(QtGui.QMainWindow):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None) :
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle("Media Player")

        # creating a basic vlc instance
        self.Instance = vlc.Instance()
        # creating an empty vlc media player
        self.MediaPlayer = self.Instance.media_player_new()

        self.songmanager = SongManager()
        self.isPaused = False
        self.createUI()
        self.songQ = SongQ()

    def createUI(self):
        """Set up the user interface, signals & slots
        """
        self.Widget = QtGui.QWidget(self)
        self.setCentralWidget(self.Widget)

        # In this widget all Options will be shown. when clicked, a subList should be open
        self.MySongs = QtGui.QListWidget()
        self.MySongs.addItem("PlayList") 
        self.MySongs.addItem("Songs")
        self.MySongs.addItem("Albums")
        self.MySongs.addItem("Artists")


        self.MySongs.itemClicked.connect(self.mySongsClicked)

        # A demo of the list for the GUI. In future, Song suggestions for a user will be in the list.
        self.SurfSong = QtGui.QListWidget()
        self.SurfSong.addItem("Song1")
        self.SurfSong.addItem("Song2")
        self.SurfSong.addItem("Song3")
        self.SurfSong.addItem("Song4")


        self.songslist = SongListWidget(self.songmanager.getSongs(), self)
        self.albumslist = AlbumListWidget(self.songmanager.getAlbums(), self)
        self.artistslist = ArtistListWidget(self.songmanager.getArtists(), self)
        self.playlist = PlaylistWidget(self.songmanager.getPlaylists(), self)
        

        self.songslist.hide()
        self.albumslist.hide()
        self.artistslist.hide()
        self.playlist.hide()


        #A Vertical layout which holds Mysong and SurfSong widget
        self.MainInterface = QtGui.QVBoxLayout()
        self.MainInterface.addWidget(self.SurfSong)
        self.MainInterface.addWidget(self.MySongs)
        self.MainInterface.addWidget(self.songslist)
        self.MainInterface.addWidget(self.albumslist)
        self.MainInterface.addWidget(self.artistslist)
        self.MainInterface.addWidget(self.playlist)


        #Slider to maintain timeline of the song
        self.PositionSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.PositionSlider.setToolTip("Position")
        self.PositionSlider.setMaximum(1000)

        self.PositionSlider.setStyleSheet(positionslidersheet)


        #Connect slider to setPosition function, when a user move the slider it should change the playing.
        self.connect(self.PositionSlider,
                     QtCore.SIGNAL("sliderMoved(int)"), self.setPosition)

        #Horizontal Box for play-pause,Stop button
        self.HButtonBox = QtGui.QHBoxLayout()
        self.PlayButton = QtGui.QPushButton("Play")
        self.HButtonBox.addWidget(self.PlayButton)

        #Connect the play button with function PlayPause()
        self.connect(self.PlayButton, QtCore.SIGNAL("clicked()"),
                     self.PlayPause)

        self.StopButton = QtGui.QPushButton("Stop")
        self.HButtonBox.addWidget(self.StopButton)

        #Connect the Stop button with the function Stop()
        self.connect(self.StopButton, QtCore.SIGNAL("clicked()"),
                     self.Stop)



        self.HButtonBox.addStretch(1)
        
        #Volume Slider 
        self.VolumeSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.VolumeSlider.setMaximum(100)
        self.VolumeSlider.setValue(self.MediaPlayer.audio_get_volume())
        self.VolumeSlider.setToolTip("Volume")
        self.HButtonBox.addWidget(self.VolumeSlider)
        
        #connect volume slider with the function setVolume()
        self.connect(self.VolumeSlider,
                     QtCore.SIGNAL("valueChanged(int)"),self.setVolume)

        #Whole layout stored in the VBoxLayout. contains each layout in the app
        self.VBoxLayout = QtGui.QVBoxLayout()
        self.VBoxLayout.addLayout(self.MainInterface)
        self.VBoxLayout.addWidget(self.PositionSlider)
        self.VBoxLayout.addLayout(self.HButtonBox)

        #Final widget which contains whole app
        self.Widget.setLayout(self.VBoxLayout)

        #making a menubar action for Open the song and exit
        open = QtGui.QAction("&Open", self)
        self.connect(open, QtCore.SIGNAL("triggered()"), self.OpenFile)
        exit = QtGui.QAction("&Exit", self)
        self.connect(exit, QtCore.SIGNAL("triggered()"), sys.exit)
        menubar = self.menuBar()
        file = menubar.addMenu("&File")
        file.addAction(open)
        file.addSeparator()
        file.addAction(exit)

        #timer to update the Position slider
        self.Timer = QtCore.QTimer(self)
        self.Timer.setInterval(200)
        self.connect(self.Timer, QtCore.SIGNAL("timeout()"),
                     self.updateUI)

    def PlayPause(self):
        """Toggle play/pause status
        """
        if self.MediaPlayer.is_playing():
            self.MediaPlayer.pause()
            self.PlayButton.setText("Play")
            self.isPaused = True
        else:
            if self.MediaPlayer.play() == -1:
                self.Play()
            self.MediaPlayer.play()
            self.PlayButton.setText("Pause")
            self.Timer.start()
            self.isPaused = False

    def Play(self):
        self.Stop()
        song = self.songQ.getSong()
        self.playFile(song.location)
        #self.OpenFile()
        self.PlayPause()
        return
            


    def Stop(self):
        """Stop player
        """
        self.MediaPlayer.stop()
        self.PlayButton.setText("Play")


    def OpenFile(self):
        """Open a media file in a MediaPlayer
        """
        filename = QtGui.QFileDialog.getOpenFileName(self,
                                                     "Open File", user.home)
        if not filename:
            return
        self.playFile(filename)


    def playFile(self,filename):
        # create the media
        self.Media = self.Instance.media_new(unicode(filename))
        # put the media in the media player
        self.MediaPlayer.set_media(self.Media)

        # parse the metadata of the file
        self.Media.parse()
        # set the title of the track as window title
        self.setWindowTitle(self.Media.get_meta(0))

        
    def setVolume(self, Volume):
        """Set the volume
        """
        self.MediaPlayer.audio_set_volume(Volume)

    def setPosition(self, Position):
        """Set the position
        """
        # setting the position to where the slider was dragged
        self.MediaPlayer.set_position(Position / 1000.0)
        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise are the results
        # (1000 should be enough)

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        self.PositionSlider.setValue(self.MediaPlayer.get_position() * 1000)

        if not self.MediaPlayer.is_playing():
            # no need to call this function if nothing is played
            self.Timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()

    def mySongsClicked(self,item):

        print "oops " + str(item.text())


        self.MySongs.hide()
        self.SurfSong.hide()

        if item.text() == "Songs":

            self.songslist.show()

        elif item.text() == "Albums":
            self.albumslist.show()

        elif item.text() == "Artists":
            self.artistslist.show()

        elif item.text() == "PlayList":
            self.playlist.show()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MediaPlayer = Player()
    MediaPlayer.show()
    MediaPlayer.resize(640, 480)
    sys.exit(app.exec_())
