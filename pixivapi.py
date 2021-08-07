import json
import random

from pixivpy3 import AppPixivAPI, PixivAPI
import pixiv_auth


def loadtoken():
    configstr = open("pixivtoken.json")
    configjson = json.load(configstr)
    return configjson


def savetoken(dict):
    with open("pixivtoken.json", "w") as fp:
        fp.write(json.dumps(dict, indent=4))
        fp.close()



def refresh_token(oldtoken):
    tokens = pixiv_auth.refresh(oldtoken)
    savetoken(tokens)


def converturl(url):
    return url.replace('pximg.net', 'pixiv.cat')

def daily_ranking(r18):
    # initialize
    aapi = AppPixivAPI()
    tokens = loadtoken()
    aapi.set_auth(tokens['access_token'], tokens['refresh_token'])

    if r18 == 0:
        json_result = aapi.illust_ranking()
        offset = 30
        illusts_array = json_result.illusts


        for i in range(2):

            json_result = aapi.illust_ranking(offset=offset)
            illusts_array += json_result.illusts
            if len(json_result.illusts) == 30:
                offset += 30
            else:
                break

    else:
        json_result = aapi.illust_ranking('day_r18')
        offset = 30
        illusts_array = json_result.illusts

        for i in range(3):
            json_result = aapi.illust_ranking('day_r18',offset=offset)
            illusts_array += json_result.illusts
            if len(json_result.illusts) == 30:
                offset += 30
            else:
                break



    maxnum = len(illusts_array)
    index = random.randint(0, maxnum-1)
    illust = illusts_array[index]
    author = illust['user']['name']
    title = illust.title
    img_url = converturl(illust.image_urls['large'])

    img_dict = {'author': author, 'title': title, 'img_url': img_url}

    return img_dict


def search_tag(tag, r18):
    # initialization
    aapi = AppPixivAPI()
    tokens = loadtoken()
    aapi.set_auth(tokens['access_token'], tokens['refresh_token'])

    json_result = aapi.search_illust(tag, search_target='partial_match_for_tags', sort='popular_desc')
    illusts_array = json_result.illusts
    offset = 30

    if len(illusts_array) == 0:
        return None

    if len(illusts_array) == 30:
        for i in range(9):
            json_result = aapi.search_illust(tag, search_target='partial_match_for_tags', sort='popular_desc', offset=offset)
            illusts_array += json_result.illusts
            if len(json_result.illusts) == 30:
                offset += 30
            else:
                break

    censored_array = censor(illusts_array)

    safe_array = censored_array['safe']
    r18_array = censored_array['r18']

    safe_index = len(safe_array)
    r18_index = len(r18_array)

#safe mode
    if r18 == 0:
        if safe_index == 0:
            return None
        index = random.randint(0, safe_index - 1)
        illust = safe_array[index]
    elif r18 == 1:
        if r18_index == 0:
            return None
        index = random.randint(0, r18_index - 1)
        illust = r18_array[index]


    author = illust['user']['name']
    title = illust.title
    img_url = converturl(illust.image_urls['large'])

    img_dict = {'author': author, 'title': title, 'img_url': img_url}

    return img_dict


def recommended():
    aapi = AppPixivAPI()
    tokens = loadtoken()
    aapi.set_auth(tokens['access_token'], tokens['refresh_token'])

    json_result = aapi.illust_recommended()
    illust_array = json_result.illusts

    max_num = len(illust_array)
    index = random.randint(0, max_num - 1)

    illust = illust_array[index]
    author = illust['user']['name']
    title = illust.title
    img_url = converturl(illust.image_urls['large'])

    img_dict = {'author': author, 'title': title, 'img_url': img_url}

    return img_dict

def censor (illusts_array):
    r18_illusts = []
    safe_illusts = []
    flag = True
    for illustr in illusts_array:

        for i in illustr['tags']:
            if i['name'] == 'R-18' or i['name'] == 'R-18G':
                r18_illusts.append(illustr)
                flag = False
                break

        if flag == True:
            safe_illusts.append(illustr)

        flag = True






    return {'safe':safe_illusts, 'r18':r18_illusts}




#shuaxin
old_token = loadtoken()['refresh_token']
refresh_token(old_token)

