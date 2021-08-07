import time

import requests
import matplotlib.pyplot as plt
import math


async def get_report():
    headers = {
        'Cookie': 'UM_distinctid=179370001841f2-025d082d4ab1df-6373664-144000-17937000185243; CNZZDATA1275376637=493204760-1620122574-%7C1620122574; _csrf=jrcYexB_eVbeUXsMEAgmdUvO; user-info=56600; SESSDATA=180d346a%2C1643214500%2Cfcd25%2A71; bili_jct=e8d3472335f91652db334260dbfdface; DedeUserID=155000; DedeUserID__ckMd5=d9f008b27ab04b17; sid=7mgv8tk0; session-api=geb2qkblr47jvr64pbv2a38l0u',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Mobile Safari/537.36',
        'Connection': 'keep-alive',
        'x-csrf-token': 'PgoaVN3z-KSVZv70a4z5E8MRn-Ze2v3UgwTI'
    }
    try:
        while True:
            r = requests.get('https://www.bigfun.cn/api/feweb?target=kan-gong-guild-report%2Fa&date=', headers=headers,
                             timeout=3)
            data = r.json()['data']
            data = sorted(data, key=lambda k: k['damage_total'], reverse=True)
            if data is not None:
                break
            time.sleep(1)
            print("get_report None触发")

   # fig, ax = plt.subplots(1, 1)
        plt.rcParams['font.sans-serif'] = ['SimHei']

        data_table = []
        if len(data) == 0:
            data_table = ["ERROR!", "", "", "", "", ""]
        else:
            for i in range(len(data)):
                username = data[i]['user_name']
                damage_num = data[i]['damage_num']
                damage_total = data[i]['damage_total']
                try:
                    first_d = str(data[i]['damage_list'][0]['damage']) + "\n" + data[i]['damage_list'][0]['boss_name']
                except:
                    first_d = ""

                try:
                    second_d = str(data[i]['damage_list'][1]['damage']) + "\n" + data[i]['damage_list'][1]['boss_name']
                except:
                    second_d = ""

                try:
                    third_d = str(data[i]['damage_list'][2]['damage']) + "\n" + data[i]['damage_list'][2]['boss_name']
                except:
                    third_d = ""

                data_table.append([username, damage_num, damage_total, first_d, second_d, third_d])

        fig1 = plt.gcf()
        column_labels = ["昵称", "出刀次数", "造成伤害", "第一刀", "第二刀", "第三刀"]
        # ax.axis('tight')
        # ax.axis('off')
        plt.axis('off')

        ytable = plt.table(cellText=data_table, colLabels=column_labels, loc="center", cellLoc="center")

        ytable.scale(1, 2)

        fig1.savefig('huizhan_report', dpi=350, bbox_inches='tight')
        plt.close()

        return data
    except:
        time.sleep(1)
        print("runtime 触发")
        data = await get_report()
        return data



async def get_names():
    headers = {
        'Cookie': 'UM_distinctid=179370001841f2-025d082d4ab1df-6373664-144000-17937000185243; CNZZDATA1275376637=493204760-1620122574-%7C1620122574; _csrf=jrcYexB_eVbeUXsMEAgmdUvO; user-info=56600; SESSDATA=180d346a%2C1643214500%2Cfcd25%2A71; bili_jct=e8d3472335f91652db334260dbfdface; DedeUserID=155000; DedeUserID__ckMd5=d9f008b27ab04b17; sid=7mgv8tk0; session-api=geb2qkblr47jvr64pbv2a38l0u',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Mobile Safari/537.36',
        'Connection': 'keep-alive',
        'x-csrf-token': 'PgoaVN3z-KSVZv70a4z5E8MRn-Ze2v3UgwTI'
    }

    try:
        while True:
            r = requests.get('https://www.bigfun.cn/api/feweb?target=kan-gong-guild-report%2Fa&date=', headers=headers,
                             timeout=3)
            data = r.json()['data']

            data = sorted(data, key=lambda k: k['damage_total'], reverse=True)

            if data is not None:
                break
            time.sleep(1)
            print("get_names None触发")


        chudao_num = len(data)

        try:
            first_name = data[0]['user_name']
        except:
            first_name = ""

        try:
            second_name = data[1]['user_name']
        except:
            second_name = ""

        try:
            third_name = data[2]['user_name']
        except:
            third_name = ""

        name_array = [first_name, second_name, third_name, chudao_num]



        return name_array
    except:
        time.sleep(1)
        print("runtime 触发")
        name_array = await get_report()
        return name_array


async def get_boss():
    headers = {
        'Cookie': 'UM_distinctid=179370001841f2-025d082d4ab1df-6373664-144000-17937000185243; CNZZDATA1275376637=493204760-1620122574-%7C1620122574; _csrf=jrcYexB_eVbeUXsMEAgmdUvO; user-info=56600; SESSDATA=180d346a%2C1643214500%2Cfcd25%2A71; bili_jct=e8d3472335f91652db334260dbfdface; DedeUserID=155000; DedeUserID__ckMd5=d9f008b27ab04b17; sid=7mgv8tk0; session-api=geb2qkblr47jvr64pbv2a38l0u',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Mobile Safari/537.36',
        'Connection': 'keep-alive',
        'x-csrf-token': 'PgoaVN3z-KSVZv70a4z5E8MRn-Ze2v3UgwTI'
    }
    try:
        while True:
            r = requests.get('https://www.bigfun.cn/api/feweb?target=kan-gong-guild-boss-info%2Fa', headers=headers,
                             timeout=3)
            data = r.json()['data']

            if data is not None:
                break
            time.sleep(1)


        round = data['round']
        boss_1 = data['boss'][0]
        boss_2 = data['boss'][1]
        boss_3 = data['boss'][2]
        boss_4 = data['boss'][3]
        boss_data = [round, boss_1, boss_2, boss_3, boss_4]

        return boss_data
    except:

        time.sleep(1)
        print("runtime 触发")
        boss_data = await get_boss()
        return boss_data



def get_boss_hpbar(boss_data, i):
    hp_1 = '🅾'
    hp_0 = '⬛'
    hp_1_num = math.ceil(boss_data[i]['remain_hp'] / boss_data[i]['total_hp'] * 10)
    hp_v = ""

    for j in range(10):
        if hp_1_num != 0:
            hp_v += hp_1
            hp_1_num -= 1
        else:
            hp_v += hp_0

    return hp_v

def get_boss_str(boss_data, i):
    boss_hpbar = get_boss_hpbar(boss_data, i)
    return"""LV.%s %s
%s/%s
%s

"""%(boss_data[i]['level'], boss_data[i]['name'], boss_data[i]['remain_hp'], boss_data[i]['total_hp'], boss_hpbar)



def get_unbattled_list(data):
    # read from file
    memberlist=[]

    f = open("member.txt", encoding='utf-8')  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        line = line.rstrip("\n")
        memberlist.append(line)
        line = f.readline()
    f.close()

    battaled_list=[]
    for i in range(len(data)):
        battaled_list.append(data[i]['user_name'])

    unmemberList=[]
    for member in memberlist:
        if member not in battaled_list:
            unmemberList.append(member)

    return unmemberList


