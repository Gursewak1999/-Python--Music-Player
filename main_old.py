import asyncio
import json
import sys
import urllib.request

from pyqt5_material import apply_stylesheet
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QListWidget
from UI import playerUI, mainUI
from misc.helpers import getSongsList, getSongDetails_online

app = QApplication(sys.argv)
window = QMainWindow()
player = playerUI.Ui_Form()
apply_stylesheet(app, theme='dark_cyan.xml')

threadQueue = list()


def onCreate():
    main_window = mainUI.Ui_MainWindow()
    main_window.setupUi(window)
    player.setupUi(main_window.player_view)
    ar = getSongsList(window)
    main_window.listView.setSizeAdjustPolicy(QListWidget.AdjustToContents)

    window.show()

    thread = runThread(loadDummySong())
    threadQueue.append(thread.run)
    thread = runThread(loadList(main_window.listView, ar))
    threadQueue.append(thread.run)

    thread = runThread(runAfter(ar))
    threadQueue.append(thread.run)
    # thread.start()

    main_window.listView.itemClicked.connect(onListItemClicked)
    # executeThreads()
    executeThreads()
    sys.exit(app.exec_())


def loadList(listView, ar):
    def load_list():
        i = 0
        for listItem in ar:
            if i == 10: break
            i = i + 1
            thread = runThread(updateUI(listItem))
            threadQueue.append(thread.run)

    def updateUI(listItem):
        def update():
            details = getSongDetails_online(listItem.name, listItem.cover, listItem.url)
            listItem.setDetails(details)
            settupLists(listView, listItem)
            listView.update()

        return update

    return load_list


def loadDummySong():
    def load_dummy_song():
        name = "Out Of Stock"
        url = "https://djyoungster.org/music/out-of-stock-jordan-sandhu-v70549.html"
        cover = "https://art.djyoungster.in/img/250x250/70549.jpg"
        details = getSongDetails_online(name, cover, url)
        thread = runThread(loadPlayer(details))
        # thread.run()
        threadQueue.append(thread.run)

    return load_dummy_song


def loadPlayer(det):
    def load_player():
        det1 = str(det).replace("'", '"')
        details = json.loads(det1)
        # load Cover
        data = urllib.request.urlopen(details['cover']).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        pixmap = pixmap.scaled(player.label_cover.size(), Qt.KeepAspectRatio,
                               transformMode=Qt.SmoothTransformation)
        player.label_cover.setPixmap(pixmap)
        player.label_name.setText(details['name'])

        player.label_ongoing_time = "00:00"
        player.label_total_time = "--:--"

        print(details['details'])

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

    return load_player


def onListItemClicked(item):
    details = item.whatsThis()
    thread = runThread(loadPlayer(details))
    # thread.run()
    threadQueue.append(thread.run)


def runAfter(ar):
    def run_after():
        print("post exec")
        for listItem in ar:
            listItem.setCover()
            listItem.graphicsView_cover.update()

    return run_after


def settupLists(myList, child):
    # Add to list a new item (item is simply an entry in your list)
    item = QListWidgetItem(myList)
    # myList.addItem(item)
    # child.widget_container.setMinimumSize(611, 107)
    item.setSizeHint(child.widget_container.size())
    item.setWhatsThis(str(child.details))

    myList.setItemWidget(item, child.widget_container)


class AThread(QThread):

    def __init__(self, function):
        super().__init__()
        self.function = function

    async def asyncRun(self):
        self.function()

    def run(self):
        asyncio.run(self.asyncRun())


def runThread(function):
    # print(function)
    thread = AThread(function)
    thread.started.connect(app.exit)
    return thread


def executeThreads():
    for thread in threadQueue:
        print(thread)
        thread()


onCreate()
