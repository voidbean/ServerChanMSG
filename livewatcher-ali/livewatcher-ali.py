import requests
import json
import os

#Server_chan的key
SCKEY = '此处填写您在 sc.ftqq.com 申请到的SCKEY'

bili_url = "http://api.bilibili.com/x/space/acc/info"
server_chan_url = f"https://sc.ftqq.com/{SCKEY}.send"

#数据字典的key为主播id, value为true或false均可
live_cache = {'692283831': 'false'}


def get_status(uid):
    return requests.get(bili_url, params={'mid': uid}).json()


def checkFlag(config):
    if config['flag'] == "true":
        return True
    else:
        return False


def send(title, message):
    requests.get(server_chan_url, params={'text': title, 'desp': message})

def cache():
    for uid in live_cache:
        resp_json = get_status(uid)
        status = resp_json['data']['live_room']['liveStatus']
        if live_cache[uid] == 'true':
            if status == 0:
                live_cache[uid] = 'false'
        else:
            if status == 1:
                live_cache[uid] = 'true'
                title = f"您关注的{resp_json['data']['name']}开播了!"
                message = f"直播标题:{resp_json['data']['live_room']['title']}\n{resp_json['data']['live_room']['url']}"
                send(title, message)

def handler(event, context):
  print('start....')
  cache()