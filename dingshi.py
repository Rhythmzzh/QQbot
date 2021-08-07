from graia.broadcast import Broadcast
from graia.application import *
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import *
from graia.scheduler import GraiaScheduler
from graia.scheduler.timers import crontabify
from graia.scheduler import timers
import asyncio
import messages

GROUP_ID_NGCS = 764157243

#message_remind = MessageChain.create([Plain('try11111\n')])

loop = asyncio.get_event_loop()	#异步循环
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
	broadcast=bcc,
	connect_info=Session(
		host='http://localhost:8080', # 填入 httpapi 服务运行的地址
		authKey='12345678', # 填入 authKey
		account=551698863, # 你的机器人的 qq 号
		websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
	)
)

# 定时任务
a = 0

b = 2
scheduler = GraiaScheduler(loop, bcc)
@scheduler.schedule(crontabify('* * * * * 1,2,3,4,5,6,7'))
async def scheduledRemindBookRoom():
	await messages.sendGroupsMessages(app=app, groups_id=[GROUP_ID_NGCS], messages=[MessageChain.create([Plain(str(a))])])

async def scheduledRemindBookRoom1():
	await messages.sendGroupsMessages(app=app, groups_id=[GROUP_ID_NGCS], messages=[MessageChain.create([Plain(str(b))])])




app.launch_blocking()
loop.run_forever()