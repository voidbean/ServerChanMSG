import schedule
import aiohttp
import asyncio
import time

#Server_chan的key
SCKEY = '此处填写您在 sc.ftqq.com 申请到的SCKEY'

bili_url = "http://api.bilibili.com/x/space/acc/info"
server_chan_url = f"https://sc.ftqq.com/{SCKEY}.send"

#数据字典的key为主播id, value为true或false均可
live_cache = {'692283831': 'false'}


async def get_status(uid):
    async with aiohttp.ClientSession() as session:
        async with session.get(bili_url, params={'mid': uid}) as resp:
            result = await resp.json()
            return result


def checkFlag(config):
    if config['flag'] == "true":
        return True
    else:
        return False


async def send(title, message):
    async with aiohttp.ClientSession() as session:
        async with session.get(server_chan_url, params={'text': title, 'desp': message}) as resp:
            return resp


async def main():
    for uid in live_cache:
        resp_json = await get_status(uid)
        status = resp_json['data']['live_room']['liveStatus']
        if live_cache[uid] == 'true':
            if status == 0:
                live_cache[uid] = 'false'
        else:
            if status == 1:
                live_cache[uid] = 'true'
                title = f"您关注的{resp_json['data']['name']}开播了!"
                message = f"直播标题:{resp_json['data']['live_room']['title']}\n{resp_json['data']['live_room']['url']}"
                await send(title, message)


def job():
    asyncio.run(main())


schedule.every(3).minutes.do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)