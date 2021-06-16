import json
import urllib.request
from time import sleep

import requests

from UI import custom_list_songs

_server_url = "http://localhost/music_api/"


def download_song(link, name):
    print('Downloadling ' + name + '...')
    res = requests.get(link)
    try:
        res.raise_for_status()
    except:
        print('Downloading Error')
        return False
    song = open(name, 'wb')

    for chunk in res.iter_content(10000):
        song.write(chunk)

    song.close()

    print('Download Comlete: ' + name + '...')

    return True


def getSongs_online():
    url = _server_url + "getTop50PunjabiSongs.php/"
    return json.loads(urllib.request.urlopen(url).read())


def getSongDetails_online(name, cover, url):
    url = _server_url + "getSongDetails.php/" + "?n=" + name + "&c=" + cover + "&p=" + url
    url = url.replace(" ", "%20")
    out = json.loads(urllib.request.urlopen(url).read())

    #print(out)
    return out
