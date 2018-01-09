import json


class Song:

    """Song class which holds info about the song

    attributes
    ===============
    - location
    - Album
    - Artist
    - Genre Tag List
    - duration (in seconds)
    - count of listening 

    """

    def __init__(self,key,value):

        self.name = key[0]
        self.album = key[1]
        self.artist = key[2]
        self.location = value["location"]
        self.duration = value["duration"]
        self.count = value["count"]
        self.taglist = value["tags"]


class Album:

    """Album class which holds the list of songs in it.!
    
    attributes
    ===============
    - Artist
    - Song object List
    - duration
    """

    def __init__(self,key,value,songpool):

        self.name = key[0]
        self.artist = key[1]
        self.songlist = {}
        for eachsongid in value["songsID"]:
            self.songlist[eachsongid] = songpool[eachsongid]

class Playlist:

    """Playlist class which holds the list of songs in it.!
    
    attributes
    ===============
    - Song object List
    - duration
    """

    def __init__(self,key,value,songpool):

        self.name = key[0]
        self.songlist = {}
        for eachsongid in value["songsID"]:
            self.songlist[eachsongid] = songpool[eachsongid]




class Artist:

    """Artist class which holds the list of songs and albums

    attributes
    ============
    - name
    - albumList
    - songList
    """

    def __init__(self,key,value,songpool,albumpool):

        self.name = key[0]

        self.songlist = {}
        for eachsongid in value["songsID"]:
            self.songlist[eachsongid] = songpool[eachsongid]

        self.albumlist = {}
        if "albumsID" in value:
            for eachalbumid in value["albumsID"]:
                self.albumlist[eachalbumid] = albumpool[eachalbumid]





class SongManager:

    """
    variables
    ===============
    1. locallist = local form of the json which is in file


    Methods
    ===========
    1. pullList(): fetch list from the file.!
    2. pushList(): store the json in the file.!
    3. getSongs(): get songs from the localist
    4. getAlbums(): get albums from the locallist
    5. getArtist(): get artists from the locallist
    6. getPlaylist(): get playlists from the locallist

    """
    def __init__(self):

        self.locallist = None

        self.pullList()

        self.songpool = {}
        for each in self.locallist["Songs"]:
            self.songpool[each] = Song(each,self.locallist["Songs"][each])

        self.albumpool = {}
        for each in self.locallist["Albums"]:
            self.albumpool[each] = Album(each,self.locallist["Albums"][each],self.songpool)

        self.artistpool = {}
        for each in self.locallist["Artists"]:
            self.artistpool[each] = Artist(each,self.locallist["Artists"][each],self.songpool,self.albumpool)

        
        self.playlistpool = {}

        for each in self.locallist["Playlists"]:
            self.playlistpool[each] = Playlist(each,self.locallist["Playlists"][each],self.songpool)


    def pullList(self):
        # with open("jsonlist.json") as file:
        #     self.locallist = json.load(file)
        
        self.locallist = {
                            "Artists": { 

                                ("Ed Sheeran",): {

                                    "songsID": [("A team","plus","Ed Sheeran")]

                                }


                            },

                            "Albums": {

                                ("plus","Ed Sheeran"): {

                                    "songsID": [("A team","plus","Ed Sheeran")]


                                }

                            },

                            "Songs": {

                                ("A team","plus","Ed Sheeran"): {

                                    "location" : "",
                                    "duration" : "",
                                    "count" : 0,
                                    "tags" : []

                                }

                            },

                            "Playlists": {

                                
                            }



                        }    



    def pushList(self):

        with open("jsonlist.json") as file:
            json.dump(self.locallist,file)

    def getSongs(self):

        return self.songpool

    
    def getAlbums(self):

        return self.albumpool
    

    def getArtists(self):

        return self.artistpool
   
    def getPlaylists(self):

        return self.playlistpool


    def addSong(self,song):

        songid = (song.name,song.album,song.artist)

        self.locallist["Songs"][songid] = song
        
        if (song.album,song.artist) in self.localist["Albums"]:
            self.localist["Albums"][(song.album,song.artist)]["songsID"].append(songid)
        else:
            self.localist["Albums"][(song.album,song.artist)] = {"songsID":[]}

        if (song.artist) in self.localist["Artists"]:
            self.localist["Artists"][(song.artist)]["songsID"].append(songid)
            
            if not (song.album,song.artist) in self.localist["Artists"][(song.artist)]["albumsID"]:
                self.localist["Artists"][(song.artist)]["albumsID"].append((song.album,song.artist))


        self.pushList()

