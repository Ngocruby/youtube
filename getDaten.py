# -*- coding: utf-8 -*-

import requests  # funktion dan link
import json  # funktion format file json


def getYoutube():
    url = 'https://restcountries.eu/rest/v2/all'
    r = requests.get(url)  #als Text lesen, verlinken
    countries = r.json()  #Format unter Json
    #Database
    videos = []
    total = {}
    # lands
    regions = []
    for country in countries:
        regions.append(country.get(
            'region'))  # region aus countries rausnehmen und zu hinzufugen
    regions = list(set(regions))  # region filter
    regions = [r for r in regions if r != '']
    regions.sort()
    print(regions)

    #genres
    #topic duoc viet duoi dang array
    topics = {
        # music
        "/m/04rlf": "Music",
        "/m/05fw6t": "Children's music",
        "/m/02mscn": "Christian music",
        "/m/0ggq0m": "Classical music",
        "/m/01lyv": "Country",
        "/m/02lkt": "Electronic music",
        "/m/0glt670": "Hip hop music",
        "/m/05rwpb": "Independent music",
        "/m/03_d0": "Jazz",
        "/m/028sqc": "Music of Asia",
        "/m/0g293": "Music of Latin America",
        "/m/064t9": "Pop music",
        "/m/06cqb": "Reggae",
        "/m/06j6l": "Rhythm and blues",
        "/m/06by7": "Rock music",
        "/m/0gywn": "Soul music",
        #gaming
        "/m/0bzvm2": "Gaming",
        "/m/025zzc": "Action game",
        "/m/02ntfj": " Action-adventure game",
        "/m/0b1vjn": " Casual game",
        "/m/02hygl": "Music video game",
        "/m/04q1x3q": "Puzzle video game",
        "/m/01sjng": " Racing video game",
        "/m/0403l3g": "Role-playing video game",
        "/m/021bp2": " Simulation video game",
        "/m/022dc6": "Sports game",
        "/m/03hf_rm": "Strategy video game",
        #sport
        "/m/06ntj": "Sports",
        "/m/0jm_": " American football",
        "/m/018jz": " Baseball",
        "/m/018w8": " Basketball",
        "/m/01cgz": " Boxing",
        "/m/09xp_": " Cricket",
        "/m/02vx4": " Football",
        "/m/037hz": "Golf",
        "/m/03tmr": "Ice hockey",
        "/m/01h7lh": "Mixed martial arts",
        "/m/0410tth": "Motorsport",
        "/m/066wd": " Professional wrestling",
        "/m/07bs0": " Tennis",
        "/m/07_53": " Volleyball",
        #entertainment
        "/m/02jjt": " Entertainment",
        "/m/095bb": " Animated cartoon",
        "/m/09kqc": " Humor",
        "/m/02vxn": "Movies",
        "/m/05qjc": " Performing arts",
        "/m/02jjt": " Entertainment",
        "/m/095bb": " Animated cartoon",
        "/m/09kqc": " Humor",
        "/m/02vxn": "Movies",
        "/m/05qjc": " Performing arts",
        #lifestyle
        "/m/019_rr": "Lifestyle",
        "/m/032tl": "Fashion",
        "/m/027x7n": "Fitness",
        "/m/02wbm": "Food",
        "/m/0kt51": "Health",
        "/m/03glg": "Hobby",
        "/m/068hy": "Pets",
        "/m/041xxh": "Physical attractiveness [Beauty]",
        "/m/07c1v": "Technology",
        "/m/07bxq": " Tourism",
        "/m/07yv9": "Vehicles",
        #others
        "/m/01k8wb": "Knowledge",
        "/m/098wr": "Society",
        "/m/0f2f9": "TV Show",
        "/m/01h6rj": "Military"
    }
    #Schleife
    index = 0
    for country in countries:
        name = country['name']
        alpha2Code = country['alpha2Code']
        alpha3Code = country['alpha3Code']
        region = country['region']
        url2 = 'https://www.googleapis.com/youtube/v3/videos?key=AIzaSyBpu8hgnXbkqFVWrAvwRUEz7T13ii3I7WM&part=snippet,topicDetails,statistics&maxResults=50&chart=mostPopular&regionCode=' + alpha2Code + '&videoCategoryId=10'
        response = requests.get(url=url2).json()
        index += 1
        print(str(index) + '/' + str(len(countries)))
        if 'items' in response:
            items = response['items']
            if len(items):
                firstVideo = items[0]
                videoObject = {}
                videoObject['alpha2Code'] = alpha2Code
                videoObject['alpha3Code'] = alpha3Code
                videoObject['region'] = region
                videoObject['name'] = name
                videoObject['video'] = firstVideo
                videoObject['items'] = items
                videos.append(videoObject)

    # Totals for Top Music Video
    for videoObject in videos:
        vID = videoObject['video']['id']
        if vID not in total:
            total[vID] = 1
        else:
            total[vID] += 1

    print(total)

    total_keys = total.keys()
    total_values = sorted(
        total.values(),
        reverse=True)  # reverse um die häufigsten Wert zu kriegen
    top = []
    for value in total_values:
        for key in total_keys:
            if total[key] == value and key not in top:
                top.append(key)
                break

    # Colors
    colors = [
        # Basic
        '#ff0000',  # Red
        '#cc0099',  # Red Violet
        '#990099',  # Violet
        '#660099',  # Blue Violet
        '#0051d4',  # Blue
        '#0bb4c3',  # Blue Green
        '#009900',  # Green
        '#66cc00',  #Yellow Green
        '#ffff00',  # Yellow
        '#ffcc00',  # Yellow Orange
        '#ff9900',  # Orange
        '#ff6600',  # Red Orange
        # White
        '#ff999a',  # Red
        '#ff99ff',  # Red Violet
        '#b89eb8',  # Violet
        '#9999cd',  # Blue Violet
        '#9accff',  # Blue
        '#99ffcd',  # Blue Green
        '#99ff99',  # Green
        '#cdfe67',  # Yellow Green
        '#ffffcd',  # Yellow
        '#feff98',  # Yellow Orange
        '#ffcc66',  # Orange
        '#ff9968',  # Red Orange
        # Gray
        '#cb7c7f',  # Red
        '#ca6699',  # Red Violet
        '#986699',  # Violet
        '#6669a',  # Blue Violet
        '#9b99ca',  # Blue
        '#5d9c9c',  # Blue Green
        '#679966',  # Green
        '#9acc99',  #Yellow Green
        '#cccb66',  # Yellow
        '#cccd32',  # Yellow Orange
        '#cc9900',  # Orange
        '#cb9966',  # Red Orange
        # Black
        '#9b0300',  # Red
        '#660032',  # Red Violet
        '#673266',  # Violet
        '#653396',  # Blue Violet
        '#003399',  # Blue
        '#006766',  # Blue Green
        '#006600',  # Green
        '#679801',  #Yellow Green
        '#999a01',  # Yellow
        '#cf9700',  # Yellow Orange
        '#cd6600',  # Orange
        '#9a3400',  # Red Orange
    ]
    overlay = {}
    index = 0
    for key in top:
        overlay[key] = {}
        overlay[key]['total'] = total[key]
        overlay[key]['color'] = colors[index]
        index += 1
    print("OVERLAY")

    # Genres For Lands um keys von topics zu nehmen(z.B./m/06ntj kann man nicht wissen, welche genre ist es)
    genresForLand = {}  #leeren objekt
    for videoObject in videos:  #schleife
        land = videoObject['name']
        items = videoObject['items']
        for item in items:
            topic = ''
            if 'topicDetails' in item:
                topicIds = item['topicDetails']['relevantTopicIds']  # Items of API

                topicIds = [x for x in topicIds
                            if x != '/m/04rlf']  #  Music Filter
                if len(topicIds):
                    topic = topicIds[0]
                else:
                    topic = '/m/04rlf'
                if land not in genresForLand:
                    genresForLand[land] = {}
                if topic not in genresForLand[land]:
                    genresForLand[land][topic] = 1
                else:
                    genresForLand[land][topic] += 1

    print(genresForLand)

    #Genres For Land2 um die value von topic zu nehmen(z.B. /m/06ntj ist sport)
    genresForLand2 = {}

    for land in genresForLand:
        genresArray = []
        for genre in genresForLand[land]:
            obj = {}
            obj['genre'] = topics[genre]
            obj['total'] = genresForLand[land][genre]
            genresArray.append(obj)
        genresForLand2[land] = genresArray

    youtube = {}

    youtube['top'] = top
    youtube['videos'] = videos
    youtube['overlay'] = overlay
    youtube['genresForLand'] = genresForLand2

    print("YOUTUBE")
    with open('./json/youtube.json', 'w') as outfile:
        json.dump(youtube, outfile)

    


getYoutube()