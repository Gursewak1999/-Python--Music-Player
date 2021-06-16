import sqlite3
from misc.helpers import getSongs_online, getSongDetails_online


class DatabaseHelper:

    def __init__(self):
        self.conn = sqlite3.connect("music-player.db")

        self.initTables()

    def initTables(self):

        isFound = False
        cur = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='songs';")
        for row in cur:
            isFound = True
            break
        if not isFound:
            self.conn.execute('''CREATE TABLE songs
                 (ID INT PRIMARY KEY     NOT NULL,
                 NAME           TEXT    NOT NULL,
                 COVER            TEXT     NOT NULL,
                 DETAILS        TEXT,
                 LINKS        TEXT);''')

    def addSong(self, details):

        id = str(details['cover']).replace("https://art.djyoungster.in/img/250x250/", "").replace(".jpg", "")

        if not self.isSongExist(details['name']):

            query = '''INSERT INTO songs 
                    (ID,NAME,COVER, DETAILS,LINKS) VALUES 
                    ("''' + id + '''",
                    "''' + details['name'] + '''", 
                    "''' + details['cover'] + '''", 
                    "", 
                    "");'''
            self.conn.execute(query)
            self.conn.commit()
            print(details['name'], id, "newly added")
        else:
            pass

    def addSongDetails(self, details):
        if not self.isSongDetailsExist(details['name']):
            self.conn.execute('''UPDATE songs 
                    SET  DETAILS="''' + str(details['details']) + '''",LINKS="''' + str(details['download_links']) + '''" 
                    WHERE NAME="''' + details['name'] + '''";''')
            self.conn.commit()
            print(details['name'] + " newly Added Details")
        else:
            pass

    def isSongExist(self, name):
        cursor = self.conn.execute('''SELECT NAME FROM songs WHERE NAME="''' + name + '''"''')
        isFound = False
        for row in cursor:
            isFound = True
        return isFound

    def isSongDetailsExist(self, name):
        cursor = self.conn.execute('''SELECT NAME,DETAILS FROM songs WHERE NAME="''' + name + '''"''')
        isFound = False
        for row in cursor:
            if row[1] != "":
                isFound = True
        return isFound

    def addSongs(self, songs_list):
        print("songs count : ", len(songs_list))
        for songs in songs_list:
            self.addSong(songs)

    def getSongs(self):
        cursor = self.conn.execute('''SELECT NAME FROM songs WHERE 1''')
        for row in cursor:
            print(row)

    def getLatestSongs(self):
        cursor = self.conn.execute('''SELECT * FROM songs WHERE 1''')
        ar = list()
        for row in cursor:
            ar.append(row)
        ar.reverse()
        return ar

    def updateSongs(self, updateWindow=None):
        songs_list = getSongs_online()

        self.addSongs(songs_list['ar'])
        # db.getSongs()
        progress = 0
        for songs in songs_list['ar']:
            self.addSongDetails(getSongDetails_online(songs['name'], songs['cover'], songs['url']))
            progress = progress + 2
            if updateWindow != None:
                updateWindow.update(progress)
            print(progress, "%")

    def close(self):

        self.conn.close()

    def updateSongsAndClose(self, updateWindow):
        self.updateSongs(updateWindow)
        self.close()
        pass


def updateSongDatabase(updateWindow):
    DatabaseHelper().updateSongsAndClose(updateWindow)
