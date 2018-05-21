import requests
import json

def getYoutube():
    url ='https://restcountries.eu/rest/v2/all'
    r = requests.get(url)
    countries = r.json()
    #Database
    videos = []
    total = {}
    #Loop
    index = 0
    for country in countries:
        name = country['name']
        alpha2Code = country['alpha2Code']
        alpha3Code = country['alpha3Code']
        url2= 'https://www.googleapis.com/youtube/v3/videos?key=AIzaSyBpu8hgnXbkqFVWrAvwRUEz7T13ii3I7WM&part=snippet&chart=mostPopular&regionCode=' + alpha2Code +'&videoCategoryId=10'
        response = requests.get(url=url2).json()
        index +=1
        print(str(index) + '/' + str(len(countries)))
        if 'items' in response:
            items = response['items']
            if len(items):
                video = items[0]
                obj = {}
                obj['alpha2Code'] = alpha2Code
                obj['alpha3Code'] = alpha3Code
                obj['name'] = name
                obj['video'] = video
                videos.append(obj)

    for v in videos: 
        vID = v['video']['id']
        if vID not in total:
            total[vID] =1
        else:
            total[vID] += 1
    	
    print(total)

    print("VIDEOS")

    with open('./json/youtube.json', 'w') as outfile:
        json.dump(videos, outfile)



    total_keys = total.keys()
    total_values = sorted(total.values(), reverse=True)
    top =[]
    for value in total_values:
        for key in total_keys:
            if total[key] == value and key not in top:
                top.append(key)
                break
    print("TOP")
    with open('./json/youtube.json', 'w') as outfile:
        json.dump(videos, outfile)

    #
    colors =[
        '#EA4335', # Red (Level 0)
            '#FBBC05', # Yellow (Level 0)
            '#4285F4', # Blue (Level 0)
            '#34A853', # Green (Level 0)
            '#551A8B', # Purple (Level 0)
            # Level 1
            '#EB5447', # Red (Level 1)
            '#FBC21B', # Yellow (Level 1)
            '#5390F5', # Blue (Level 1)
            '#46AF62', # Green (Level 1)
            '#642E95', # Purple (Level 1)
            # Level 2
            '#ED6559', # Red (Level 2)
            '#FBC832', # Yellow (Level 2)
            '#649BF6', # Blue (Level 2)
            '#58B772', # Green (Level 2)
            '#7343A0', # Purple (Level 2)
            # Level 3
            '#EF766C', # Red (Level 3)
            '#FCCE49', # Yellow (Level 3)
            '#75A6F7', # Blue (Level 3)
            '#6BBF81', # Green (Level 3)
            '#8358AA', # Purple (Level 3)
            # Level 4
            '#F1877E', # Red (Level 4)
            '#FCD45F', # Yellow (Level 4)
            '#86B1F8', # Blue (Level 4)
            '#7DC791', # Green (Level 4)
            '#926DB5', # Purple (Level 4)
            # Level 5
            '#F39890', # Red (Level 5)
            '#FCDA76', # Yellow (Level 5)
            '#97BCF9', # Blue (Level 5)
            '#90CFA1', # Green (Level 5)
            '#A282BF', # Purple (Level 5)
            # Level 6
            '#F5A9A3', # Red (Level 6)
            '#FDE08D', # Yellow (Level 6)
            '#A9C7FA', # Blue (Level 6)
            '#A2D7B0', # Green (Level 6)
            '#B196CA', # Purple (Level 6)
            # Level 7
            '#F7BAB5', # Red (Level 7)
            '#FDE6A4', # Yellow (Level 7)
            '#FDE6A4', # Blue (Level 7)
            '#B5DFC0', # Green (Level 7)
            '#C1ABD4', # Purple (Level 7)
            # Level 8
            '#F9CBC7', # Red (Level 8)
            '#FDECBA', # Yellow (Level 8)
            '#CBDDFC', # Blue (Level 8)
            '#C7E7D0', # Green (Level 8)
            '#D0C0DF', # Purple (Level 8)
            # Level 9
            '#FBDCDA', # Red (Level 9)
            '#FEF2D1', # Yellow (Level 9)
            '#DCE8FD', # Blue (Level 9)
            '#DAEFDF', # Green (Level 9)
            '#E0D5E9', # Purple (Level 9)
    ]
    overlay = {}
    index = 0
    for key in top:
        overlay[key] = {}
        overlay[key]['total'] = total[key]
        overlay[key]['color'] = colors[index]
        index +=1
    print("OVERLAY")
    with open('./json/youtube.json', 'w') as outfile:
        json.dump(overlay, outfile)
    youtube = {}
    youtube['top'] = top
    youtube['videos'] = videos
    youtube['overlay'] = overlay
    print("YOUTUBE")
    with open('./json/youtube.json', 'w') as outfile:
        json.dump(youtube, outfile)
    print('END')

getYoutube()