import requests
import time
from datetime import datetime
import streamlit as st

def correct_time(time_in):
    time_struct_UTC = time.gmtime(time_in)
    time_out = time.mktime(time_struct_UTC) + 8 * 60 * 60
    timestamp = str(datetime.fromtimestamp(time_out))
    return timestamp

def read_user_info(key):
    with open('UserInfo.txt', 'r') as file:
        Lst_txt = file.readlines()
    csrf = ''
    csrf_token =''
    cookie = ''
    for txt in Lst_txt:
        Lst_data = txt.split('//')
        if Lst_data[0] == key:
            csrf = Lst_data[1]
            csrf_token = Lst_data[2]
            cookie = Lst_data[3].replace('\n', '')
            break
    return csrf, csrf_token, cookie

def write_user_info(key, csrf, csrf_token, cookie):
    txt_write = '//'.join([key, csrf, csrf_token, cookie])
    with open('UserInfo.txt', 'w') as file:
        file.write(txt_write)

def read_data(key):
    with open('Data.txt', 'r') as file:
        Lst_txt = file.readlines()
    status = ''
    timestamp =''
    for txt in Lst_txt:
        Lst_data = txt.split(',')
        if Lst_data[0] == key:
            status = int(Lst_data[1])
            timestamp = Lst_data[2]
    return status, timestamp

def write_data(key, status, timestamp):
    txt_write = ','.join([key, str(status), timestamp])
    with open('Data.txt', 'w') as file:
        file.write(txt_write)

#---//Set the basic info//---
st.title("弹幕宠物挂机脚本1")
custom_basic = st.checkbox("自定义基本设定", False)
if custom_basic:
    url = st.text_input("B站API网址", value = 'https://api.live.bilibili.com/msg/send')
    hd_origin = st.text_input("Origin", value = 'https://live.bilibili.com')
    hd_priority = st.text_input("Priority", value = 'u=1, i')
    hd_user_agent = st.text_input("User-Agent", value = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')
else:
    url = 'https://api.live.bilibili.com/msg/send'
    hd_origin = 'https://live.bilibili.com'
    hd_priority = 'u=1, i'
    hd_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'

#---//Set the user info//---
st.markdown("---")
st.header("用户基本信息")
user_id = st.text_input("用户名", value = 'Koziu')
is_search = st.checkbox("查询", False)
if is_search:
    #---//Search the user info in data//---
    [csrf_ini, csrf_token_ini, cookie_ini] = read_user_info(user_id)
    csrf = st.text_input("csrf", value = csrf_ini)
    csrf_token = st.text_input("csrf_token", value = csrf_token_ini)
    cookie = st.text_input("Cookie", value = cookie_ini)

    #---//Set the headers//---
    headers = {'Cookie': cookie, 'Origin': hd_origin, 'Priority': hd_priority, 'User-Agent': hd_user_agent}

    #---//Update the new user info to data//---
    request_update = st.checkbox("更新", False)
    if request_update:
        is_update = st.button("确认更新（谨慎）")
        if is_update:
            write_user_info(user_id, csrf, csrf_token, cookie)
else:
    headers = None


#---//Set the custom info//---
st.markdown("---")
st.header("修炼信息")
id_room = st.text_input("直播间号", value = '')
txt = st.text_input("发送内容", value = '修炼')
secs_step = float(st.text_input("发送间隔(s)", value = '600'))
[status_user, time_last] = read_data(user_id)
if st.button("切换状态"):
    status_user *= -1
    write_data(user_id, status_user, time_last)
if status_user == 1:
    st.metric("当前状态", "修炼中", correct_time(int(time_last)))
else:
    st.metric("当前状态", "空闲中", correct_time(int(time_last)))

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
if id_room and headers:
    while status_user == 1:
        is_send_real = False
        time_now = int(time.time())
        if time_last:
            secs_passed = time_now - int(time_last)
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
                st.write("发送成功" + str(time_now))
            else:
                st.write("发送失败")
            time_last = str(time_now)
            write_data(user_id, status_user, time_last)
