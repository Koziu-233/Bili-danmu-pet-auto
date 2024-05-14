import requests
import time
from datetime import datetime
import streamlit as st

def correct_time(time_in):
    time_struct_UTC = time.gmtime(time_in)
    time_out = time.mktime(time_struct_UTC) + 8 * 60 * 60
    timestamp = str(datetime.fromtimestamp(time_out))
    return timestamp

#---//Set the basic info//---
st.title("弹幕宠物挂机脚本")
custom_basic = st.checkbox("自定义基本设定", False)
if custom_basic:
    url = st.text_input("B站API网址", value = 'https://api.live.bilibili.com/msg/send')
else:
    url = 'https://api.live.bilibili.com/msg/send'

#---//Set the user info//---
st.markdown("---")
st.header("用户基本信息")
csrf = st.text_input("csrf", value = 'b51b8ad084d831c3af20f4fc6b1c3a51')
csrf_token = st.text_input("csrf_token", value = 'b51b8ad084d831c3af20f4fc6b1c3a51')
cookie = st.text_input("Cookie", value = 'buvid3=EC72F8C4-ED97-73A1-59BB-203FDFBC330853369infoc; b_nut=1714394553; _uuid=31F6CEEC-B3A5-214E-16B7-8C104A2410A3CE49817infoc; buvid4=A72633C4-3F55-D30D-24C9-CA2C8AF166D554070-024042912-0X4ynfGMIH8tT1jBmQsVL9k5PnRi4lPacrD5VArjsCsQFU7KapjYSV1rIZMjg4ur; enable_web_push=DISABLE; rpdid=0zbfAHJtrd|voDS695l|1VJ|3w1S1qlx; DedeUserID=14180802; DedeUserID__ckMd5=31f1b9e161535495; header_theme_version=CLOSE; LIVE_BUVID=AUTO9917143987942530; hit-dyn-v2=1; CURRENT_QUALITY=120; fingerprint=8d3de7cc9f5fb6fbd4839664a54ec7cd; buvid_fp_plain=undefined; CURRENT_BLACKGAP=0; bp_video_offset_14180802=926939584176062535; CURRENT_FNVAL=4048; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTU2OTg3NTgsImlhdCI6MTcxNTQzOTQ5OCwicGx0IjotMX0.cPcWdzQ-iC8A5-EO5yX1VZbez9PfgTYOvbqinEkBwqo; bili_ticket_expires=1715698698; buvid_fp=8d3de7cc9f5fb6fbd4839664a54ec7cd; SESSDATA=50bbfbc7%2C1730995989%2Cd208b%2A51CjDdYEqE-9DZrpt3N1XRqrGJ2pnD1EIMmLUp67YLQUA0LS_fKx0WWwj9KxAj_ECf6DASVkp4bVZlc2gzQUhXakQwUmM5QlhLSDU1RURsVVhtXzlaaEFydkxyWlkzY0duNUhFcjlrZTJMQ0dYajc4bXM2cXg4d056UzFqT0dwdXhiRXduRldWSkx3IIEC; bili_jct=b51b8ad084d831c3af20f4fc6b1c3a51; sid=827wyk7i; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1715360621,1715436942,1715447926,1715489769; home_feed_column=5; browser_resolution=2560-1305; bp_t_offset_14180802=930517863140163601; Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1715493502; PVID=1; b_lsid=10FCB28FB_18F6B7AA255; bsource=search_baidu')

#---//Set the headers//---
headers = {
    'Cookie': cookie,
    'Origin': 'https://live.bilibili.com',
    'Priority': 'u=1, i',
    'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': 'Windows',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

#---//Set the custom info//---
st.markdown("---")
st.header("修炼信息")
id_room = st.text_input("直播间号", value = '')
txt = st.text_input("发送内容", value = '修炼')
secs_step = float(st.text_input("发送间隔(s)", value = '600'))
is_start = st.checkbox("开始修炼", False)

#---//Calculate remaining time//---
st.markdown("---")
st.header("估算突破所需时间")
num_remain = st.text_input("升级所需内力", value = '')
num_step = st.text_input("升级所需内力", value = '17')
if num_remain:
    secs_all = float(num_remain) / float(num_step) * 10
    time_finish = int(time.time()) + secs_all
    time_fin_show = correct_time(time_finish)
    st.write("估算可突破时间为" + time_fin_show)

#---//Send the request//---
if is_start and id_room:
    time_last = None
    while is_start:
        is_send_real = False
        time_now = int(time.time())
        if time_last:
            secs_passed = time_now - time_last
            if secs_passed >= secs_step:
                is_send_real = True
        else:
            is_send_real = True
        if is_send_real:
            time_send = '{}'.format(time_now)
            data = {
                'bubble': '0',
                'msg': txt,
                'color': '16777215',
                'mode': '1',
                'roomtype': '0',
                'jumpfrom': '84001',
                'reply_mid': '0',
                'reply_attr': '0',
                'replay_dmid': '',
                'statistics': {'appId': '100','platform': '5'},
                'fontsize': '25',
                'rnd': time_send,
                'roomid': id_room,
                'csrf': csrf,
                'csrf_token': csrf_token
            }
            response = requests.post(url, data = data, headers = headers)
            code_return = response.status_code
            if code_return == 200:
                time_show = correct_time(time_now)
                st.write("发送成功" + time_show)
            else:
                st.write("发送失败")
            time_last = time_now
