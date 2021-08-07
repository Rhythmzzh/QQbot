import random
import requests
import re

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'referer': 'https://www.pixiv.net/ranking.php?mode=daily&content=illust',
}

path = 'D:/'
repeat = 1


def getSinglePic(url):
    global repeat
    response = requests.get(url, headers=headers, timeout=3)
    # 提取图片名称
    name = re.search('"illustTitle":"(.+?)"', response.text)
    name = name.group(1)
    if re.search('[\\\ \/ \* \? \" \: \< \> \|]', name) != None:
        name = re.sub('[\\\ \/ \* \? \" \: \< \> \|]', str(repeat), name)
        repeat += 1
    # 提取图片原图地址
    picture = re.search('"regular":"(.+?)"},"tags"', response.text)

    url_c = picture.group(1)

    url_d = re.findall('^(.+?)","or', url_c)
    url_d = url_d[0]
    url_d = url_d.replace('pximg.net', 'pixiv.cat')

    #url_d 地址


    return url_d


def getAllPicUrl():

    n = random.randint(1,10)
    url = 'https://www.pixiv.net/ranking.php?mode=daily&content=illust&p=%d&format=json' % n


    response = requests.get(url, headers=headers)
    illust_id = re.findall('"illust_id":(\d+?),', response.text)

    picUrl = ['https://www.pixiv.net/artworks/' + i for i in illust_id]

    pic_index = random.randint(0, len(picUrl))
    picUrl_single = picUrl[pic_index]


    return getSinglePic(picUrl_single)

