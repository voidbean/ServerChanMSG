import requests
import re

#Server_chan的key
SCKEY = '此处填写您在 sc.ftqq.com 申请到的SCKEY'
#b站用户的uid, 多个id逗号分割
bili_live_idx = ['692283831']
#ytb上的channelId, 具体值可以通过页面点进去后的url获得
ytb_live_idx = ['UCMmpLL2ucRHAXbNHiCPyIyg', 'UCrwJvtphcyux30pAgoX68jA']

bili_url = "http://api.bilibili.com/x/space/acc/info"
ytb_url = "https://www.youtube.com/channel"
server_chan_url = f"https://sc.ftqq.com/{SCKEY}.send"

live_cache = {}
CEHCK_FALG = 'icon":{"iconType":"LIVE"}'




def get_bili_status(uid):
    return requests.get(bili_url, params={'mid': uid}).json()

def get_ytb_status(channelId):
    REGEX = f'(?<="channelId":"{channelId}","title":)".*"(?=,"navigationEndpoint")'
    result = {'status':'0'}
    resp = requests.get(f'{ytb_url}/{channelId}').text
    match = re.findall(REGEX, resp)
    if match is not None:
        result['title'] = match
    if CEHCK_FALG in resp:
        result['status'] = '1'
    return result

def send(title, message):
    requests.get(server_chan_url, params={'text': title, 'desp': message})

def cache():
    for uid in bili_live_idx:
        resp_json = get_bili_status(uid)
        status = resp_json['data']['live_room']['liveStatus']
        if uid not in live_cache:
            live_cache[uid] = 'false'
        if live_cache[uid] == 'true':
            if status == 0:
                live_cache[uid] = 'false'
        else:
            if status == 1:
                live_cache[uid] = 'true'
                title = f"您关注的{resp_json['data']['name']}开播了!"
                message = f"直播标题:{resp_json['data']['live_room']['title']}\n{resp_json['data']['live_room']['url']}"
                send(title, message)
    for channel_id in ytb_live_idx:
        result = get_ytb_status(channel_id)
        if channel_id not in live_cache:
            live_cache[channel_id] = 'false'
        if live_cache[channel_id] == 'true':
            if result['status'] == '0':
                live_cache[channel_id] = 'false'
        else:
            if result['status'] == '1':
                live_cache[channel_id] = 'true'
                title = f"您关注的{result['title']}开播了!"
                message = "开播通知"
                send(title, message)

def handler(event, context):
  print('start....')
  cache()
