import json
from random import Random

from UI import custom_list_songs
from misc.DatabaseHelper import DatabaseHelper

db = DatabaseHelper()


def convert(det):
    details = dict()
    # print(det)
    details['id'] = det[0]
    details['name'] = det[1]
    details['cover'] = det[2]
    details['details'] = json.loads(det[3].replace("'", '"'))
    details['links'] = json.loads(det[4].replace("'", '"'))
    return details


def getSongsList(window):
    ar = db.getLatestSongs()
    prefab_ar = list()

    for dat in ar:
        listPrefab = custom_list_songs.Ui_Form()
        listPrefab.setupUi(window)
        listPrefab.setDetails(convert(dat))
        prefab_ar.append(listPrefab)
    return prefab_ar


def getRandomSong():
    songs = db.getLatestSongs()
    return convert(songs[Random().randint(a=0, b=len(songs) - 1)])
