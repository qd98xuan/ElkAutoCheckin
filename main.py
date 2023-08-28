# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import urllib3
import datetime
import demjson3 as demjson
import os

http = urllib3.PoolManager()
# USER_NAME = ''
# USER_PASSW = ''

USER_NAME = os.environ['USERNAME']
USER_PASSW = os.environ['PASSWORD']
USER_DOMAIN = os.environ['DOMAIN']


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# 自动签到
def elk_checkin():
    elk_login()


# 登录
def elk_login():
    res = http.request('POST', USER_DOMAIN+'/auth/login',
                       fields={'email': USER_NAME, 'passwd': USER_PASSW, 'remember_me': 'on'})
    print(demjson.decode(res.data))
    if demjson.decode(res.data)['msg'] == "登录成功":
        print('登录成功-' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        cookies = res.headers["Set-Cookie"].replace(" path=/,", "")
        print(cookies)
        elk_open_user(cookies)
    else:
        print(demjson.decode(res.data)['msg'])


# 打开用户页面
def elk_open_user(cookies):
    data = http.urlopen(method='GET', url=USER_DOMAIN+'/user',
                        headers={'Cookie': cookies})
    # print(data.data.decode())
    checkin(cookies)


# 签到
def checkin(cookies):
    resp = http.request('POST', USER_DOMAIN+'/user/checkin', headers={'Cookie': cookies})
    respData = demjson.decode(resp.data)
    print(respData)
    print(respData["msg"])
    # print(resp)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    elk_checkin()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
