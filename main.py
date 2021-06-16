import json
import sys
import urllib.request
from PyQt5.QtCore import Qt, QRunnable, QThreadPool
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QVBoxLayout, QWidget, QLabel
from qt_material import apply_stylesheet
from UI import playerUI, mainUI
from misc.DatabaseHelper import updateSongDatabase
from misc.MusicPlayer import media_player
from misc.songsHelper import getRandomSong, getSongsList, db


app = QApplication(sys.argv)
window = QMainWindow()

player = playerUI.Ui_Form()

apply_stylesheet(app, theme='dark_cyan.xml')

list_childs = getSongsList(window)
main_window = mainUI.Ui_MainWindow()


def onCreate():
    main_window.setupUi(window)
    player.setupUi(main_window.player_view)
    main_window.listView.setSizeAdjustPolicy(QListWidget.AdjustToContents)
    window.show()
    init()


class Thread(QRunnable):

    def __init__(self, func):
        super().__init__()
        self.func = func

    def run(self) -> None:
        self.func()

    def startPool(self):
        QThreadPool.globalInstance().start(self)


def init():
    # init Lists and UI

    th = Thread(loadPlayer(getRandomSong()))
    th.startPool()

    media_player.attachUI(player)
    # init lists
    main_window.listView.itemClicked.connect(onSongClick)
    Thread(loadList(main_window.listView, list_childs)).startPool()
    # loadList(main_window.listView, list_childs)()

    # init Covers
    Thread(runAfter(list_childs)).startPool()


def runAfter(ar):
    def run_after():
        for listItem in ar:
            listItem.setCover()
            listItem.graphicsView_cover.update()

    return run_after


playThread = None


def onSongClick(view):
    global playThread
    playThread = Thread(loadPlayer(view.whatsThis()))
    playThread.startPool()


def loadPlayer(det):
    def load_Player():
        det1 = str(det).replace("'", '"')
        details = json.loads(det1)
        media_player.playNewSong(details['links'][0].get("48"))

        # load Cover
        data = urllib.request.urlopen(details['cover']).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        pixmap = pixmap.scaled(player.label_cover.size(), Qt.KeepAspectRatio,
                               transformMode=Qt.SmoothTransformation)
        player.label_cover.setPixmap(pixmap)
        player.label_name.setText(details['name'])

        player.label_ongoing_time.setText("00:00")
        player.label_total_time.setText("--:--")

        player.label_details1.setText("SINGERS : " + details['details'][0].get("SINGERS"))
        player.label_details2.setText("LYRICIST : " + details['details'][1].get("LYRICIST"))
        player.label_details3.setText("COMPOSER : " + details['details'][2].get("COMPOSER"))

        player.label_cover.update()
        player.label_name.update()
        #        player.label_ongoing_time.update()
        #        player.label_total_time.update()
        player.label_details1.update()
        player.label_details2.update()
        player.label_details3.update()

    return load_Player


def loadList(listView, ar):
    def load_list():
        for listItem in ar:
            # Thread(updateUI(listItem)).startPool()
            updateUI(listItem)()

    def updateUI(listItem):
        def update():
            settupLists(listView, listItem)
            listView.update()

        return update

    return load_list


def settupLists(myList, child):
    # Add to list a new item (item is simply an entry in your list)
    item = QListWidgetItem(myList)

    item.setSizeHint(child.widget_container.size())
    item.setWhatsThis(str(child.details))

    myList.setItemWidget(item, child.widget_container)


class UpdateWindow(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Updating Songs Database .... ... .")
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update(self, progress):
        self.label.setText("Updating Songs Database .... " + str(progress) + "%")


def updateSongs(updateWindow):
    def fun():
        updateSongDatabase(updateWindow)

    return fun


if len(db.getLatestSongs()) == 0:
    updateWindow = UpdateWindow()
    updateWindow.show()
    updateSongDatabase(updateWindow)
    onCreate()
else:
    onCreate()
    updateWindow = UpdateWindow()
    updateWindow.show()
    Thread(updateSongs(updateWindow)).startPool()
app.exec_()
