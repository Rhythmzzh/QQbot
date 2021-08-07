from graia.application import GraiaMiraiApplication
from graia.application.message.chain import MessageChain
from graia.application.group import Group
import asyncio

async def sendGroupsMessages(app, groups_id, messages):
	groups = await app.groupList()
	for group in groups:
		if (group.id in groups_id):
			for message in messages:
				await app.sendGroupMessage(group, message)