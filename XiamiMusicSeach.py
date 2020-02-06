# coding=utf-8
import requests


def Gethttp(key):
    try:
        url = 'https://api.xiami.com/web?v=2.0&app_key=1&key=' + key + '&page=1&limit=20&_ksTS=1517295011073_76&r=search/songs'
        print(url)
        headers = {"referer": "https://h.xiami.com/index.html?f=&from="}
        res = requests.get(url, headers=headers).text
        res = res.encode('utf-8').decode('unicode_escape').replace('\/', '/')
        return res
    except:
        print('查询失败！')


if __name__ == '__main__':
    data = '演员'
    res = Gethttp(data)
