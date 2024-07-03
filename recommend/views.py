from django.shortcuts import render
import json
import urllib.request
import urllib.parse
import random
import musicbrainzngs as mb
from . import keys
from django.http import JsonResponse


def searchMovie(request):
    if request.method == "GET":
        search = str(urllib.parse.quote(request.GET.get("term")))
        if search:
            # Get movie ID from Search
            id = urllib.request.urlopen(
                "https://api.themoviedb.org/3/search/movie?api_key="
                + keys.api_key
                + "&language=en-US&query="
                + search
                + "&page=1&include_adult=false"
            ).read()
            id_data = json.loads(id)
            id = []
            x = 0
            for i in id_data["results"]:
                id.append(str(id_data["results"][x]["title"]))
                x = x + 1

            return JsonResponse(id, safe=False)
        else:
            id = []
            movie = ""


def getMovie(request):
    if request.method == "POST":
        movie = str(urllib.parse.quote(request.POST.get("search")))
        # Get movie ID from Search
        id = urllib.request.urlopen(
            "https://api.themoviedb.org/3/search/movie?api_key="
            + keys.api_key
            + "&language=en-US&query="
            + movie
            + "&page=1&include_adult=false"
        ).read()
        id_data = json.loads(id)
        id = ""
        id = str(id_data["results"][0]["id"])

        # Get the recommendations
        res = urllib.request.urlopen(
            "https://api.themoviedb.org/3/movie/"
            + id
            + "/recommendations?api_key="
            + keys.api_key
            + "&language=en-US&page=1"
        ).read()
        json_data = json.loads(res)
    else:
        movie = ""
        json_data = {}
        id = {}

    return render(request, "index.html", {"json_data": json_data})


def searchSongs(request):
    if request.method == "GET":
        track = str((urllib.parse.quote(request.GET.get("term"))))
        id = []
        res = urllib.request.urlopen(
            "https://ws.audioscrobbler.com/2.0/?method=track.search&track="
            + track
            + "&api_key="
            + keys.lastfm_key
            + "&format=json"
        ).read()
        json_data = json.loads(res)
        x = 0
        for i in json_data["results"]["trackmatches"]["track"]:
            id.append(
                str(
                    json_data["results"]["trackmatches"]["track"][x]["name"]
                    + " - "
                    + json_data["results"]["trackmatches"]["track"][x]["artist"]
                )
            )
            x = x + 1

        return JsonResponse(id, safe=False)
    else:
        id = []


def getCovers(info):
    covers = []
    mb.set_useragent("Recommender", "1.0", "contact")
    for i in info["tracks"]:
        track = str(urllib.parse.quote(i["name"]))
        artist = str(urllib.parse.quote(i["artist"]["name"]))
        track2 = i["name"]
        artist2 = i["artist"]["name"]
        mbid = ""
        try:
            mbid = i["mbid"]
        except:
            pass
        res = urllib.request.urlopen(
            "https://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key="
            + keys.lastfm_key
            + "&artist="
            + artist
            + "&track="
            + track
            + "&format=json"
        ).read()
        json_data = json.loads(res)
        try:
            covers.append(json_data["track"]["album"]["image"][3]["#text"])
        except:
            if mbid:
                resp = urllib.request.urlopen(
                    "https://coverartarchive.org/release/" + mbid
                ).read()
                json_data_id = json.load(resp)
                print(json_data_id)
                covers.append(json_data_id["images"][0]["thumbnails"]["large"])
            else:
                try:
                    search = track2 + " - " + artist2
                    result = mb.search_releases(search, 3)
                    mbid = result["release-list"][0]["id"]
                    image_src = mb.get_image_list(mbid)
                    covers.append(image_src["images"][0]["thumbnails"]["large"])
                except:
                    covers.append("/static/placeholder.webp")

    return covers


def getSongs(request):
    if request.method == "POST":
        search = str(request.POST.get("search")).split(" - ")
        artist = str((urllib.parse.quote(search[1])))
        res = urllib.request.urlopen(
            "https://ws.audioscrobbler.com/2.0/?method=artist.getSimilar&artist="
            + artist
            + "&limit=10&api_key="
            + keys.lastfm_key
            + "&format=json"
        ).read()
        artist = []
        x = 0
        json_data = json.loads(res)
        for i in json_data["similarartists"]["artist"]:
            artist.append(json_data["similarartists"]["artist"][x]["name"])
            x += 1
        x = 0
        json_data_s = {}
        json_data_s["tracks"] = []
        for i in artist:
            res = urllib.request.urlopen(
                "https://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist="
                + str(urllib.parse.quote(i))
                + "&limit=2&api_key="
                + keys.lastfm_key
                + "&format=json"
            ).read()
            json_data = json.loads(res)
            for y in range(2):
                x += 1
                json_data_s["tracks"].append(json_data["toptracks"]["track"][y])
            if x == 16:
                break
        random.shuffle(json_data_s["tracks"])
        covers = getCovers(json_data_s)
        x = 0
        for i in covers:
            json_data_s["tracks"][x]["image"] = covers[x]
            x += 1

    else:
        json_data = {}
        json_data_s = []

    return render(request, "index.html", {"json_data_s": json_data_s})


def index(request):
    return render(request, "index.html")
