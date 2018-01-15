class SongQ:

    """
    song queue class the holds the queue that is going to be  played

    attributes:
    =================
    - song list (Queue)

    methods:
    =================

    - song append from start
    - song append from last
    - append song in shuffle mode from start
    - delete song
    - shift to first
    - get the current song
    - isnext


    """


    def __init__(self):

        self.queue = []


    def addStart(self, songlist):

        self.queue = songlist + self.queue

    def addEnd(self, songlist):

        self.queue = self.queue + songlist

    def deletesong(self, song):

        try:
            self.queue.remove(song)
        except:
            pass

    def goToStart(self, song):

        self.deletesong(song)
        self.addStart(song)

    def getSong(self):

        if len(self.queue) > 0:
            return self.queue.pop(0)


    