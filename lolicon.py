import random
import requests

def geturl(r18):
    data = requests.get('https://api.lolicon.app/setu/v2', params={'r18': r18, 'size': 'regular'})
    information = data.json()['data']
    return information[0]

def geturl_tag(r18,tag):
    data = requests.get('https://api.lolicon.app/setu/v2', params={'r18': r18, 'size': 'regular', 'tag': tag})
    information = data.json()['data']
    return information[0]


def get_ten_urls(r18):
    data = requests.get('https://api.lolicon.app/setu/v2', params={'r18': r18, 'size': 'regular', 'num': 10})
    setu = data.json()['data']
    setu_ten = []
    for s in setu:
        setu_ten.append([s['tags'][0]+", "+s['tags'][1]+", " + s['tags'][2],s['urls']['regular']])
    return setu_ten

def getmenhera():
    mhr_num = random.randint(1, 160)
    if mhr_num <= 120:
        mhr_str = str(mhr_num)+".jpg"
    else:
        mhr_str = str(mhr_num)+".png"

    return mhr_str

