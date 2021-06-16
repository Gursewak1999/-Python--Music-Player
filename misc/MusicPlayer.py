from pathlib import Path
from time import sleep
import requests
import vlc
from PyQt5.QtCore import QRunnable, QThreadPool

noPlaying = True


class Thread(QRunnable):

    def __init__(self, func):
        super().__init__()
        self.func = func

    def run(self) -> None:
        self.func()

    def startPool(self):
        QThreadPool.globalInstance().start(self)


def getFileSize(path):
    # "misc/chitt/chitt_0.mp3"
    return Path(path).stat().st_size


class MediaPlayer():
    i = 0

    def __init__(self):
        self.isPaused = False
        self.playerUI = None
        self.isPlaying = False
        self.buffer = 1000000
        self.name = "cache.mp3"
        self.player = vlc.MediaPlayer(self.name)

    def download_song_and_play(self, link):

        self.isPaused = False
        if self.player.is_playing():
            self.player.stop()

        if self.i == 0:
            self.i = 1
            self.name = "cache.mp3"
        else:
            self.i = 0
            self.name = "cache1.mp3"

        self.player = vlc.MediaPlayer(self.name)

        def fun():

            print('Downloadling ' + self.name + '...')
            noPlaying = True
            res = requests.get(link)
            try:
                res.raise_for_status()
            except:
                print('Downloading Error')
                return False

            song = open(self.name, 'wb')

            for chunk in res.iter_content(1000):
                song.write(chunk)

            try:
                self.player.play()
                sleep(.1)
                if self.player.is_playing():
                    self.isPlaying = True
                    noPlaying = False
                    sleep(.1)
                    self.updateUI()
                print("playing")
            except:
                print("error")

            song.close()

            print('Download Comlete: ' + self.name + '...')

        return fun

    def playNewSong(self, url):
        self.isPlaying = False
        Thread(self.download_song_and_play(url)).startPool()

    def playSong(self, button):
        print("clicked")
        if not self.isPaused:
            self.isPaused = True
            self.player.play()
            self.playerUI.button_play.setIcon(self.playerUI.icon_pause)
        else:
            self.isPaused = False
            self.player.pause()
            self.playerUI.button_play.setIcon(self.playerUI.icon_play)

    def attachUI(self, playerUI):
        self.playerUI = playerUI
        self.playerUI.button_play.clicked.connect(self.playSong)

    def updateUI(self):
        print("Updating UI")
        max = self.player.get_length()
        self.playerUI.label_total_time.setText(convertToTime(max))
        while self.isPlaying:
            self.playerUI.label_ongoing_time.setText(convertToTime(self.player.get_time()))
            self.playerUI.horizontalSlider_progress_bar.setValue(convertToPercentage(self.player.get_time(), max))


def convertToTime(i):
    i = i / 1000
    m = int(i / 60)
    s = int(i % 60)

    if m < 10:
        m = "0" + str(m)
    else:
        m = str(m)

    if s < 10:
        s = "0" + str(s)
    else:
        s = str(s)

    return m + " : " + s


def convertToPercentage(i, max):
    p = int(i * 100 / max)
    return p


media_player = MediaPlayer()
