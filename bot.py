import json

from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio

from graia.application.message.elements.internal import At, Plain, Image, AtAll
from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt.waiter import Waiter
from graia.application.event.messages import GroupMessage

import random
import huizhan
import messages
from graia.scheduler import GraiaScheduler
from graia.scheduler.timers import crontabify
import dyanmic as dy
import lolicon as loli
import huizhan as hz
import pixivapi

loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080",  # 填入 httpapi 服务运行的地址
        authKey="12345678",  # 填入 authKey
        account=551698863,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)
inc = InterruptControl(bcc)

# -----------------------复制线-----------------------------------------------------

# 好友私聊

@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend, message: MessageChain):
    global setu_flag
    if message.asDisplay() == "打开涩图":
        setu_flag = True
        await app.sendFriendMessage(friend, MessageChain.create([Plain("涩图功能已开启")]))

    if message.asDisplay() == "关闭涩图":
        setu_flag = False
        await app.sendFriendMessage(friend, MessageChain.create([Plain("涩图功能已关闭")]))

    # asSendable 方法将MessageChain对象转为可发送的状态


# join方法将两个MessageChain对象连接起来


# 变量

ghzFlag = True
fudu = ""
fudu_num = 0
setu_flag = True
setu_num = 1
mrsetu_num = 1
slsetu_num = 1
pixiv_daily_num = 1
pixiv_tag_num = 1
pixiv_rec_num = 1
setu_index = 0


def loadconfig():
    configstr = open("botconfig.json")
    configjson = json.load(configstr)
    return configjson


def writeconfig(dict):
    with open("botconfig.json", "w") as fp:
        fp.write(json.dumps(dict, indent=4))
        fp.close()


@bcc.receiver("GroupMessage")
async def groupMessage(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
    global ghzFlag
    global setu_num
    global fudu_num
    global fudu
    global mrsetu_num
    global slsetu_num
    global pixiv_daily_num
    global pixiv_tag_num
    global pixiv_rec_num

    if message.asDisplay() == "妹妹还活着吗":
        await app.sendGroupMessage(group, MessageChain.create([Plain("我在哦~")]))

    if message.asDisplay().startswith("-p"):
        pic = message.asDisplay()[2:]
        await app.sendGroupMessage(group, MessageChain.create([
            Image.fromLocalFile("images/" + pic)
        ]))

    if message.asDisplay() == "-关闭公会战提醒":
        ghzFlag = False
        await app.sendGroupMessage(group, MessageChain.create([Plain("已关闭公会战提醒！")]))
    if message.asDisplay() == "-打开公会战提醒":
        ghzFlag = True
        await app.sendGroupMessage(group, MessageChain.create([Plain("已开启公会战提醒！")]))

    # 妹妹用法
    if message.asDisplay().startswith("妹妹用法"):
        help = """妹妹Ver 1.9 命令指南：
-------------------------------------

妹妹还活着吗：    测试命令

-打开公会战提醒： 如上，包括每日定时报表和提醒

-关闭公会战提醒： 如上

随机涩图：       发送随机涩图

每日涩图：       随机从pixiv每日榜单发送一张图（涩度随机，共CD）

涩图十连：       什？涩图也有十连？

单抽：          垫刀优选

十连：          垫刀优选

抽卡统计：       查看抽卡概率

千里眼：        供优质抽卡参考

会战报表：       看看谁是你会一哥 (接口原因概率失败)

boss血量：      此功能已删除（别偷辣别偷辣别偷辣别偷辣）

谁没出刀：       偷偷看看谁没出刀

-------------------------------------
"""

        await app.sendGroupMessage(group, MessageChain.create([Plain(help)]))

    # 管理员命令 以后优化
    if message.asDisplay().startswith("-setu"):
        if member.id == 467528270:
            setu_num_t = message.asDisplay().split(" ")
            setu_num = int(setu_num_t[1])
            mrsetu_num = int(setu_num_t[1])
            slsetu_num = int(setu_num_t[1])
            pixiv_rec_num = int(setu_num_t[1])
            pixiv_tag_num = int(setu_num_t[1])
            pixiv_daily_num = int(setu_num_t[1])

            finalmsg = "妹妹又发现了" + setu_num_t[1] + "张新涩图哦！"
        else:
            finalmsg = "乌乌 妹妹不认识你鸭。"
        await app.sendGroupMessage(group, MessageChain.create([Plain(finalmsg)]))

    # 被at
    if message.has(At) and message.getFirst(At).target == app.connect_info.account:
        await app.sendGroupMessage(group,
                                   MessageChain.create([Image.fromLocalFile("images/menhera/" + loli.getmenhera())]))

    # 色图
    # 自用r18
    if message.asDisplay() == "随机涩图r18" and member.id == 467528270:
        setu = loli.geturl('1')
        author = setu['author']
        title = setu['title']
        url = setu['urls']['regular']
        msgchain = MessageChain.create([Plain("title: " + title + "\nauthor: " + author)])
        imgchain = MessageChain.create([Image.fromNetworkAddress(url)])
        finalmsg = msgchain.join(imgchain, msgchain.asSendable())
        await app.sendGroupMessage(group, finalmsg)

    # 群用
    if message.asDisplay() == "随机涩图":
        if setu_flag:
            # 次数判定
            if setu_num > 0:
                setu = loli.geturl('0')
                author = setu['author']
                title = setu['title']
                url = setu['urls']['regular']
                if url != None:
                    msgchain = MessageChain.create([Plain("title: " + title + "\nauthor: " + author)])
                    imgchain = MessageChain.create([Image.fromNetworkAddress(url)])
                    finalmsg = msgchain.join(imgchain, msgchain.asSendable())
                    setu_num -= 1
                    await app.sendGroupMessage(group, finalmsg)



            else:
                await app.sendGroupMessage(group, MessageChain.create([Plain("呜呜呜，妹妹累了，妹妹不想发涩图了(cd: 5min)")]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([Plain("涩图功能被妹妹吃掉辣~")]))

    # 色图十连
    if message.asDisplay() == "涩图十连":
        if setu_flag:
            # 次数判定
            if slsetu_num > 0:
                setu_ten = loli.get_ten_urls(0)
                setu_ten_str = "妹妹不知道从哪搞来了10张涩图：\n\n"
                for i in range(len(setu_ten)):
                    setu_ten_str += str(i+1) + ". " + setu_ten[i][0] + "\n"
                setu_ten_str += "\n输入相应数字开启你的涩图宝盒~ (1-10)"



                await app.sendGroupMessage(group, MessageChain.create([
                    Plain(setu_ten_str), At(member.id)
                ]))

                #中断

                @Waiter.create_using_function([GroupMessage])
                def waiter(
                        event: GroupMessage, waiter_group: Group,
                        waiter_member: Member, waiter_message: MessageChain
                ):
                    if all([
                        waiter_group.id == group.id,
                        waiter_member.id == member.id,
                    ]):

                        global setu_index
                        setu_index = waiter_message.asDisplay()

                        return event

                await inc.wait(waiter)



                try:
                    url = setu_ten[int(setu_index)-1][1]
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain("妹妹走向了"+setu_index+"号涩图盲盒并准备打开")
                    ]))

                    await app.sendGroupMessage(group, MessageChain.create([
                        At(member.id), Plain("你点的涩图到啦~"), Image.fromNetworkAddress(url)
                    ]))

                    slsetu_num -= 1
                except:
                    await app.sendGroupMessage(group, MessageChain.create([
                        At(member.id), Plain("妹妹似乎听不懂你在说什么，转头离开了...")
                    ]))



            else:
                await app.sendGroupMessage(group, MessageChain.create([Plain("呜呜呜，妹妹累了，妹妹不想发涩图了(cd: 5min)")]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([Plain("涩图功能被妹妹吃掉辣~")]))





    # pixiv每日色图
    '''
    if message.asDisplay() == "每日涩图":
        if setu_flag:
            # 次数判定
            if mrsetu_num > 0:
                url = pixiv_daily.getAllPicUrl()

                if url != None:
                    finalmsg = MessageChain.create([Image.fromNetworkAddress(url)])
                    mrsetu_num -= 1
                    await app.sendGroupMessage(group, finalmsg)



            else:
                await app.sendGroupMessage(group, MessageChain.create([Plain("呜呜呜，妹妹累了，妹妹不想发涩图了(cd: 5min)")]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([Plain("涩图功能被妹妹吃掉辣~")]))

    '''


    # pixiv功能！！！！ 使用接口
    #日榜
    if message.asDisplay() == "涩图日榜":
        if setu_flag:
            if pixiv_daily_num > 0:
                img_dict = pixivapi.daily_ranking(0)
                author = 'author: ' + img_dict['author']
                title = 'title: ' + img_dict['title']
                info = title + "\n" + author
                img_url = img_dict['img_url']

                msgchain = MessageChain.create([Image.fromNetworkAddress(img_url), Plain(info)])
                pixiv_daily_num -= 1
                await app.sendGroupMessage(group, msgchain)


            else:
                await app.sendGroupMessage(group, MessageChain.create([Plain("呜呜呜，妹妹累了，妹妹不想发涩图了(cd: 5min)")]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([Plain("涩图功能被妹妹吃掉辣~")]))



    # 日榜r18
    if message.asDisplay() == 'gg日榜':
        img_dict = pixivapi.daily_ranking(1)
        author = 'author: ' + img_dict['author']
        title = 'title: ' + img_dict['title']
        info = title + "\n" + author
        img_url = img_dict['img_url']

        msgchain = MessageChain.create([Image.fromNetworkAddress(img_url), Plain(info)])
        await app.sendGroupMessage(group, msgchain)

    # tag
    if message.asDisplay().startswith('涩图tag'):
        if setu_flag:
            if pixiv_tag_num > 0:
                tag = message.asDisplay().split(' ')[1]

                img_dict = pixivapi.search_tag(tag, 0)
                if img_dict is not None:
                    author = 'author: ' + img_dict['author']
                    title = 'title: ' + img_dict['title']
                    info = title + "\n" + author
                    img_url = img_dict['img_url']

                    msgchain = MessageChain.create([Image.fromNetworkAddress(img_url), Plain(info)])
                    pixiv_tag_num -= 1
                    await app.sendGroupMessage(group, msgchain)
                else:
                    msgchain = MessageChain.create([Plain("没有找到这个tag哦~")])
                    await app.sendGroupMessage(group, msgchain)
            else:
                await app.sendGroupMessage(group, MessageChain.create([Plain("呜呜呜，妹妹累了，妹妹不想发涩图了(cd: 5min)")]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([Plain("涩图功能被妹妹吃掉辣~")]))



    if message.asDisplay().startswith('gggg'):
        tag = message.asDisplay().split(' ')[1]
        img_dict = pixivapi.search_tag(tag, 1)

        if img_dict is not None:
            author = 'author: ' + img_dict['author']
            title = 'title: ' + img_dict['title']
            info = title + "\n" + author
            img_url = img_dict['img_url']

            msgchain = MessageChain.create([Image.fromNetworkAddress(img_url), Plain(info)])
            await app.sendGroupMessage(group, msgchain)
        else:
            msgchain = MessageChain.create([Plain("没有找到这个tag哦~")])
            await app.sendGroupMessage(group, msgchain)



    # 推荐
    if message.asDisplay() == '涩图推荐':
        if setu_flag:
            if pixiv_rec_num > 0:
                img_dict = pixivapi.recommended()
                author = 'author: ' + img_dict['author']
                title = 'title: ' + img_dict['title']
                info = title + "\n" + author
                img_url = img_dict['img_url']

                msgchain = MessageChain.create([Image.fromNetworkAddress(img_url), Plain(info)])
                pixiv_rec_num -= 1
                await app.sendGroupMessage(group, msgchain)
            else:
                await app.sendGroupMessage(group, MessageChain.create([Plain("呜呜呜，妹妹累了，妹妹不想发涩图了(cd: 5min)")]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([Plain("涩图功能被妹妹吃掉辣~")]))







    # 复读

    temp = message.asDisplay()

    if temp == fudu:
        fudu_num += 1
        if fudu_num >= 3:

            fudu_num = 0
            if temp != "[图片]":
                if (random.random() <= 0.3):
                    await app.sendGroupMessage(group, MessageChain.create([Plain(temp)]))


    else:
        fudu = temp



    # 抽卡相关
    # 单抽
    if message.asDisplay() == "单抽":
        dict = loadconfig()

        p = random.random()
        if p <= 0.0275:
            msg = "歪日，单抽出白！！"
            dict['white'] += 1
            msgchain = MessageChain.create([At(member.id), Plain(msg)])
            imgchain = MessageChain.create([Image.fromLocalFile("images/white.jpg")])
            finalmsg = msgchain.join(imgchain, msgchain.asSendable())
        if 0.0275 < p <= 0.2175:
            msg = "✴️不亏，抬走！"
            dict['yellow'] += 1
            finalmsg = MessageChain.create([At(member.id), Plain(msg)])
        if p > 0.2175:
            msg = "❇️，抬走！"
            dict['green'] += 1
            finalmsg = MessageChain.create([At(member.id), Plain(msg)])

        writeconfig(dict)
        await app.sendGroupMessage(group, finalmsg)

    # 十连
    if message.asDisplay() == "十连":

        dict = loadconfig()

        green = "❇️"
        yellow = "✴️"
        white = "⬜"
        white_num = 0
        rdmArray = []
        rdmstr = "\n"
        for i in range(10):
            rdmArray.append(random.random())

        for i in range(0, 5):
            if rdmArray[i] <= 0.0275:
                rdmstr = rdmstr + white + " "
                white_num += 1
                dict['white'] += 1
            if 0.0275 < rdmArray[i] <= 0.2175:
                rdmstr = rdmstr + yellow + " "
                dict['yellow'] += 1
            if rdmArray[i] > 0.2175:
                rdmstr = rdmstr + green + " "
                dict['green'] += 1

        rdmstr += "\n"

        for i in range(5, 9):
            if rdmArray[i] <= 0.0275:
                rdmstr = rdmstr + white + " "
                white_num += 1
                dict['white'] += 1
            if 0.0275 < rdmArray[i] <= 0.2175:
                rdmstr = rdmstr + yellow + " "
                dict['yellow'] += 1
            if rdmArray[i] > 0.2175:
                rdmstr = rdmstr + green + " "
                dict['green'] += 1

        if rdmArray[9] <= 0.0275:
            rdmstr = rdmstr + white + " "
            white_num += 1
            dict['white'] += 1
        else:
            rdmstr = rdmstr + yellow + " "
            dict['yellow'] += 1

        if white_num == 0:
            rdmstr += "\n标准剧情，抬走！"
        elif white_num == 1:
            rdmstr += "\n白盒辣！"
        elif white_num == 2:
            rdmstr += "\n歪日双白？？"
        else:
            rdmstr += "\n我程序都不敢这么写？？？？？？？？"

        writeconfig(dict)

        finalmsg = MessageChain.create([At(member.id), Plain(rdmstr)])
        await app.sendGroupMessage(group, finalmsg)

    # 抽卡统计
    if message.asDisplay() == "抽卡统计":
        dict = loadconfig()
        white_num = dict['white']
        yellow_num = dict['yellow']
        green_num = dict['green']

        total = white_num + yellow_num + green_num

        white_p = round((float(white_num / total)) * 100, 2)
        yellow_p = round((float(yellow_num / total)) * 100, 2)
        green_p = round((float(green_num / total)) * 100, 2)

        msg = "抽卡次数共计:" + str(total) + "次\n"
        msg += "❇️共计: " + str(green_num) + "   概率:" + str(green_p) + "\n"
        msg += "✴️共计: " + str(yellow_num) + "   概率:" + str(yellow_p) + "\n"
        msg += "⬜共计: " + str(white_num) + "   概率:" + str(white_p) + "\n"
        msg += "欢迎挑战数学"
        finalmsg = MessageChain.create([Plain(msg)])
        await app.sendGroupMessage(group, finalmsg)

    # 千里眼
    if message.asDisplay() == "千里眼":
        await app.sendGroupMessage(group, MessageChain.create([
            Image.fromLocalFile("images/qly.jpg")
        ]))


    #周边
    if message.asDisplay() == "周边":
        await app.sendGroupMessage(group, MessageChain.create([
            Image.fromLocalFile("images/zhoubian.jpg")
        ]))


    # 会战报表
    if message.asDisplay() == "会战报表":
        await app.sendGroupMessage(group, MessageChain.create([
            Plain("报表生成中~ （妹妹摸鱼中）")
        ]))

        data = await hz.get_report()
        member_num = len(data)
        await app.sendGroupMessage(group, MessageChain.create([
            Image.fromLocalFile("huizhan_report.png"),
            Plain("目前出刀人数共计：%s人~" % (member_num))
        ]))

    # boss血量
    if message.asDisplay() == "boss血量":
        boss_data = await hz.get_boss()

        # 可视化
        boss_str = "当前轮次： 第%s轮\n\n" % (boss_data[0])
        boss_str += hz.get_boss_str(boss_data, 1)
        boss_str += hz.get_boss_str(boss_data, 2)
        boss_str += hz.get_boss_str(boss_data, 3)
        boss_str += hz.get_boss_str(boss_data, 4)
        boss_str += "求求你们别偷辣别偷辣别偷辣！！！"
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(boss_str)
        ]))

    # 未出刀人员
    if message.asDisplay() == "谁没出刀":
        data = await huizhan.get_report()
        unmemberlist = huizhan.get_unbattled_list(data)

        msg = "呜呜呜，你们几个今天还没有出刀鸭...\n\n"
        for member in unmemberlist:
            msg = msg + member + "\n"

        msg += "\n呜呜呜你们几个今天记得出刀鸭,,,,实在不行明天也行,,,要不然后天也行,,,要不然大后天,,,\n妹妹永远等着你们鸭！"

        finalmsg = MessageChain.create([Image.fromLocalFile("images/cry.gif"), Plain(msg)])

        await app.sendGroupMessage(group, finalmsg)


# 定时
GROUP_ID_NGCS = 784142210

scheduler = GraiaScheduler(loop, bcc)


# 33竞技场
@scheduler.schedule(crontabify('0 12,19 * * * 0'))
async def jjc():
    jjcDay = loadconfig()['day']

    if jjcDay == 1:
        msg = "嗨嗨嗨！ 你醒啦！33竞技场开始了喔！~！\n今天是赛季最后一天辣!!!!!!!\n今天是赛季最后一天辣!!!!!!!\n今天是赛季最后一天辣!!!!!!!\n没打的快打 蹭低保哦！"
        msgchain = MessageChain.create([AtAll(), Plain(msg)])
    else:
        msg = "嗨嗨嗨！ 你醒啦！33竞技场开始了喔！~！\n距离本赛季结束还有" + str(jjcDay) + "天哦~"
        msgchain = MessageChain.create([Plain(msg)])
    imgchain = MessageChain.create([Image.fromLocalFile("images/jjc.gif")])
    finalmsg = msgchain.join(imgchain, msgchain.asSendable())
    await messages.sendGroupsMessages(app=app, groups_id=[GROUP_ID_NGCS], messages=[finalmsg])


# 公会战
@scheduler.schedule(crontabify('0 23 * * * 0'))
async def ghc():
    if ghzFlag:

        three_names = await hz.get_names()
        data = await hz.get_report()
        bymsg = '今日会战报表在这哦~\n' + '第一名： ' + three_names[0] + "\n" + '第二名： ' + three_names[1] + "\n" + "第三名： " + \
                three_names[2]
        bymsg = bymsg + "\n你们三个好厉害鸭！亲亲~ "
        bymsg = bymsg + "\n今天出刀人数共计：" + str(three_names[3]) + "人， 还没出刀的懒狗， 妹妹要揍你们了嗷"
        bymsgchain = MessageChain.create([Plain(bymsg)])
        byimgchain = MessageChain.create([Image.fromLocalFile("huizhan_report.png")])
        byfinalchain = bymsgchain.join(byimgchain, bymsgchain.asSendable())
        await messages.sendGroupsMessages(app=app, groups_id=[GROUP_ID_NGCS], messages=[byfinalchain])

        unmemberlist = huizhan.get_unbattled_list(data)

        msg = "呜呜呜，你们几个今天还没有出刀鸭...\n\n"
        for member in unmemberlist:
            msg = msg + member + "\n"

        msg += "\n呜呜呜你们几个今天记得出刀鸭,,,,实在不行明天也行,,,要不然后天也行,,,要不然大后天,,,\n妹妹永远等着你们鸭！"

        finalmsg = MessageChain.create([Image.fromLocalFile("images/cry.gif"), Plain(msg)])

        await messages.sendGroupsMessages(app=app, groups_id=[GROUP_ID_NGCS], messages=[finalmsg])


# 每日更新
@scheduler.schedule(crontabify('0 0 * * * 0'))
async def endofday():
    dict = loadconfig()
    jjcDay = dict['day']

    if jjcDay == 1:
        dict['day'] = 7
    else:
        dict['day'] = jjcDay - 1
    msg = "很喜欢G神的一句话《今天是个平安夜》，祝大家白盒。"
    imgchain = MessageChain.create([Image.fromLocalFile("images/danchou.gif")])
    msgchain = MessageChain.create([Plain(msg)])
    finalmsg = msgchain.join(imgchain, msgchain.asSendable())
    await messages.sendGroupsMessages(app=app, groups_id=[GROUP_ID_NGCS], messages=[finalmsg])
    writeconfig(dict)


# 动态推送
@scheduler.schedule(crontabify('0,30 * * * * 0'))
async def dynamic():
    card = await dy.getCardStr()
    id = card[0]
    dict = loadconfig()

    if id != dict['dynamic_id']:
        dict['dynamic_id'] = id

        if card[2] != "None":
            imgchain = MessageChain.create([Image.fromNetworkAddress(card[2])])
        else:
            imgchain = MessageChain.create([Image.fromLocalFile("images/danchou.gif")])

        context = card[1] + "\n" + "https://t.bilibili.com/" + str(id)

        msgchain = MessageChain.create([Plain(context)])

        finalmsg = msgchain.join(imgchain, msgchain.asSendable())

        await messages.sendGroupsMessages(app=app, groups_id=[GROUP_ID_NGCS], messages=[finalmsg])
        writeconfig(dict)

    old_token = pixivapi.loadtoken()['refresh_token']
    pixivapi.refresh_token(old_token)


@scheduler.schedule(crontabify('*/5 * * * *'))
async def setuupdate():
    global setu_num
    global mrsetu_num
    global slsetu_num
    global pixiv_daily_num
    global pixiv_tag_num
    global pixiv_rec_num

    setu_num = 1
    mrsetu_num = 1
    slsetu_num = 1
    pixiv_daily_num = 1
    pixiv_tag_num = 1
    pixiv_rec_num = 1


#三张涩图
@scheduler.schedule(crontabify('0 14 * * * 0'))
async def postthird():
    img_dict = pixivapi.daily_ranking_first()['third']
    author = 'author: ' + img_dict['author']
    title = 'title: ' + img_dict['title']
    info = '涩图时间到了~本张图是PIXIV排行榜日榜的第三名哦~\n\n'
    info += title + "\n" + author
    img_url = img_dict['img_url']

    msgchain = MessageChain.create([Image.fromNetworkAddress(img_url), Plain(info)])
    await messages.sendGroupsMessages(app=app, groups_id=[GROUP_ID_NGCS], messages=[msgchain])

@scheduler.schedule(crontabify('0 17 * * * 0'))
async def postsecond():
    img_dict = pixivapi.daily_ranking_first()['second']
    author = 'author: ' + img_dict['author']
    title = 'title: ' + img_dict['title']
    info = '涩图时间到了~本张图是PIXIV排行榜日榜的第二名哦~\n\n'
    info += title + "\n" + author
    img_url = img_dict['img_url']

    msgchain = MessageChain.create([Image.fromNetworkAddress(img_url), Plain(info)])
    await messages.sendGroupsMessages(app=app, groups_id=[GROUP_ID_NGCS], messages=[msgchain])

@scheduler.schedule(crontabify('0 20 * * * 0'))
async def postfirst():
    img_dict = pixivapi.daily_ranking_first()['first']
    author = 'author: ' + img_dict['author']
    title = 'title: ' + img_dict['title']
    info = '锵锵锵！~本张图是PIXIV排行榜日榜的第一名哦~\n\n'
    info += title + "\n" + author
    img_url = img_dict['img_url']

    msgchain = MessageChain.create([Image.fromNetworkAddress(img_url), Plain(info)])
    await messages.sendGroupsMessages(app=app, groups_id=[GROUP_ID_NGCS], messages=[msgchain])








app.launch_blocking()
loop.run_forever()





