#Diese Datei ist für das Retrieval der Daten für Music Map und BarChart
# -*- coding: utf-8 -*-
# Funktion "requets" und " json" werden erstmals importiert 
import requests  # Funktion um Link zu verlinken
import json  # Funktion um die Datei zu json zu formatieren

# Restcountries.eu erhält die ID, Alphacode von den Ländern. Wir wollen die Daten von den Länder herausnehmen und mit den YouTube API verlinken.
# Funktion wird here definieren
def getYoutube():
    url = 'https://restcountries.eu/rest/v2/all' #Variable url ist eine URL von Restcountries
    r = requests.get(url)  #als Text lesen, verlinken
    countries = r.json()  #Format unter Json
    #Database
    videos = [] #Wir stellen ein leeres Array videos um
    total = {} #Wir stellen ein leere Objekt totals um

    #Schleife für die Übernehmung des Country-ID und -Alphacode in Restcountries zum YouTube-API
    #Schleife fängt von erste Position(0) an 
    #Aus der Erstellung der Schleife des Json Datei  erhalten wir alle alpha2Code, die wir nachher für den API (url2) verwenden. Schließlich kriegen wir eine Objekt „videoObject“, welches alle Ländern der Welt erhält. In jedem Land des Objektes gibt es alpha2Code, alpha3Code, region, name, video (das Topvideo) und items(die 50 Topvideos).
    index = 0
    for country in countries:
        name = country['name']
        #alpha2code und alpha3code sind von Restcountries
        alpha2Code = country['alpha2Code'] 
        alpha3Code = country['alpha3Code']
        url2 = 'https://www.googleapis.com/youtube/v3/videos?key=AIzaSyBpu8hgnXbkqFVWrAvwRUEz7T13ii3I7WM&part=snippet,topicDetails,statistics&maxResults=50&chart=mostPopular&regionCode=' + alpha2Code + '&videoCategoryId=10'
        response = requests.get(url=url2).json()
        index += 1
        print(str(index) + '/' + str(len(countries))) # zu beoachten das Prozess
        if 'items' in response:
            items = response['items']
            if len(items):
                firstVideo = items[0]
                videoObject = {}
                videoObject['alpha2Code'] = alpha2Code
                videoObject['alpha3Code'] = alpha3Code
                videoObject['name'] = name
                videoObject['video'] = firstVideo
                videoObject['items'] = items
                videos.append(videoObject)

    # Totals for Top Music Video
    #Diese Schleife ist für die Häufigkeit des Videos zählen
    for videoObject in videos:
        vID = videoObject['video']['id'] #wir stellen neue Variable: vID,die ID von jedem Video repräsentiert.
        if vID not in total: #wenn vID noch nicht im Objekt-total ist, dann ist es gleich 1
            total[vID] = 1
        else:
            total[vID] += 1 #wenn vID schon im Objekt-total ist, dann plus 1

    print(total)
    #die Anzahl der Häufigkeit des Videos sortieren
    total_keys = total.keys()
    total_values = sorted( #ordnen ID des Videos nach der aufstiegenden Häufigkeit zu 
        total.values(),
        reverse=True)  # reverse um den häufigsten Wert zu kriegen, sonst bekommen wir der aufstiegende Wert
    
    #Array von Top Music Videos erstellen
    top = [] 
    for value in total_values:
        for key in total_keys:
            if total[key] == value and key not in top:
                top.append(key)
                break

    # Colors: Wir haben festgelegt, dass Farbe Rot als die am meinsten geschaute MV repräsentiert. Die folgende Stelle sind Lila, Blau, Green, Yellow, Orange.
    # CSS Farbesname
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
    #ordnen Farbe nach der abstiegenden Häufigkeit des Länders zu
    overlay = {} 
    index = 0
    for key in top:
        overlay[key] = {} 
        overlay[key]['total'] = total[key] #den Value aus dem Objekt-total anhand des Keys und zuweisen zu overlay[key]['total'] herausnehmen 
        overlay[key]['color'] = colors[index] #den Value aus dem Objekt-colors anhand des Keys und zuweisen zu overlay[key]['color'] herausnehmen 
        index += 1
    print("OVERLAY")

    # GenresForLands um keys von topics zu nehmen(z.B./m/06ntj)
    genresForLand = {}  #genresforLand als leeren objekt erstellen
    
    for videoObject in videos:
        land = videoObject['name'] # das Key "Name" von jedem videoObjekt herausnehmen 
        items = videoObject['items'] #das Key "items" von jedem videoObjekt herausnehmen 
        for item in items: #Schleife in items
            topic = ''
            if 'topicDetails' in item:
                topicIds = item['topicDetails']['relevantTopicIds']  # die Genre-ID von jedem Video und zuweisen zu Variable-topicIds herausnehmen 
                # Manche MusikVideo hat mehrere Genres, einer von diesen ist nur "Music". Wir versuchen die Genre "Music" zu vermeiden. 
                topicIds = [x for x in topicIds
                            if x != '/m/04rlf'] #/m/04rlf ist Genre "Music"  
                if len(topicIds): #Falls topicIds existiert,
                    topic = topicIds[0] #wir nehmen das Topic in der erste Position
                else:
                    topic = '/m/04rlf' #wenn nicht, nehmen wir troztdem /m/04rlf (Music)
                # Wenn variable land nicht in Objekt genresForLand, dann erstellen wir das leeres Objekt land in genresForLand
                if land not in genresForLand: 
                    genresForLand[land] = {}
                # Falls variable topic nicht in Objekt genresForLand, wenn das Topic noch nicht auftaucht, wird es als Wert 1 festgelegt, sonst +1 addiert.
                if topic not in genresForLand[land]:
                    genresForLand[land][topic] = 1  #wenn vID noch nicht im Objekt-total ist, dann ist es gleich 1
                else:
                    genresForLand[land][topic] += 1#wenn vID schon im Objekt-total ist, dann ist plus 1

    print(genresForLand)

    #Genres For Land2 um die value von topic zu nehmen(z.B. /m/06ntj kann man nicht wissen, welche genre es ist. Hier in genresForLand2 werden wir wissen, dass /m/06ntj Sport ist)
       
    genresForLand2 = {}

# Objekt-topics erhält alle genres, die in Youtube ist
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

#Diese Schleife ist um die gesamte Genre für bestimmte Land sortieren.
    for land in genresForLand:
        genresArray = []
        for genre in genresForLand[land]:
            obj = {}
            obj['genre'] = topics[genre] #den Value (Name von Genres) aus dem Objekt-Topics anhand des Keys und zuweisen zum obj['genre'] herausnehmen 
            obj['total'] = genresForLand[land][genre] #den Value (Häufigkeit von Genres) aus dem Objekt-genresForLand und zuweisen zum obj['total'] herausnehmen 
            genresArray.append(obj) # Objekt-obj zu genresArray hinzufügen
        genresForLand2[land] = genresArray  #zuweisen zu genresforLand2[land]

# Wir stellen neue Objekt und dann alle Daten darein zuweisen
    
    youtube = {} # Wir stellen neue Objekt-youtube 

    youtube['top'] = top # Array-Top zum Key " youtube['top']" hinzufügen 
    youtube['videos'] = videos # Array-videos zum Key " youtube['videos']" hinzufügen 
    youtube['overlay'] = overlay #  Array-Top zum Key " youtube['overlay']" hinzufügen 
    youtube['genresForLand'] = genresForLand2 # Array-Top zum Key " youtube['genresForLand']" hinzufügen 

    print("YOUTUBE")
    with open('./json/youtube.json', 'w') as outfile: # wir speichern die Daten in einem nachträglichen Json-Datei (youtube.json)
        json.dump(youtube, outfile)

    


getYoutube() #  Funktion läuft