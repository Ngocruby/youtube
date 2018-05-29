import requests  # funktion dan link
import json  # funktion format file json


def getYoutube():
    url = 'https://restcountries.eu/rest/v2/all' 
    r = requests.get(url) #als Text lesen, verlinken
    countries = r.json() #Format unter Json
    #Database
    videos = []
    total = {}
    # regions
    regions = []
    for country in countries:
        regions.append(country.get('region'))#"region" aus "countries" rausnehmen und zu "regions=[]" hinzufügen 
    regions = list(set(regions)) #region filter
    regions = [r for r in regions if r != '']
    regions.sort()
    print(regions)
    #genres
    #topic duoc viet duoi dang array
    topics = {
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
        "/m/0gywn": "Soul music"
    }
    #Schleife
    index = 0
    for country in countries:
        name = country['name']
        alpha2Code = country['alpha2Code']
        alpha3Code = country['alpha3Code']
        region = country['region']
        url2 = 'https://www.googleapis.com/youtube/v3/videos?key=AIzaSyBpu8hgnXbkqFVWrAvwRUEz7T13ii3I7WM&part=snippet,topicDetails&chart=mostPopular&regionCode=' + alpha2Code + '&videoCategoryId=10'
        response = requests.get(url=url2).json()
        index += 1
        print(str(index) + '/' + str(len(countries)))
        if 'items' in response:
            items = response['items']
            if len(items):
                video = items[0]
                obj = {}
                obj['alpha2Code'] = alpha2Code
                obj['alpha3Code'] = alpha3Code
                obj['region'] = region
                obj['name'] = name
                obj['video'] = video
                videos.append(obj)

    # Genres
    genres = {}
    for v in videos:
        topicIds = v['video']['topicDetails']['relevantTopicIds'] #nhung Item o API
        topicIds = [x for x in topicIds if x != '/m/04rlf'] # loc Music
        topic = '' #cái này là string mới đc đặt và rỗng
        if len(topicIds):# độ dài của topicIds phải tồn tại
            topic = topicIds[0]#gắn giá trị đầu tiên của topicIds vào topic
        else:
            topic = '/m/04rlf'
        if topic not in genres:
            genres[topic] = 1
        else:
            genres[topic] += 1
    # Totals
    for v in videos:
        vID = v['video']['id']
        if vID not in total:
            total[vID] = 1
        else:
            total[vID] += 1

    print(total)

    total_keys = total.keys()
    total_values = sorted(total.values(), reverse=True)
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
        '#cdfe67',  #Yellow Green
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

    youtube = {}
    #youtube['genres'] = genres
    youtube['top'] = top
    youtube['videos'] = videos
    youtube['overlay'] = overlay
    
    print("YOUTUBE")
    with open('./json/youtube.json', 'w') as outfile:
        json.dump(youtube, outfile)
   # print('END')

    top_genres = []
    
    for genre in genres:
        obj = {}
        obj['genre'] = topics[genre]
        obj['total'] = genres[genre]
        top_genres.append(obj)

    print("chart")
    with open('./json/chart.json', 'w') as outfile:
        json.dump(top_genres, outfile)
     #print('END')


getYoutube()