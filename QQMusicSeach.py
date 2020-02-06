# coding=utf-8
import json
import os
from urllib import request, parse


# 搜索请求
def getSongList(name):
    try:
        name = parse.quote(name)
        url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=68200167999648105&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w=" + name + "&g_tk=907445169&loginUin=10670374&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
        res = request.urlopen(url).read().decode('utf-8')
        res = json.loads(res)['data']['song']['list']
        return res
    except:
        print('请求失败！')


# 处理返回的json数据并打印输出列表
def PrintList(list):
    try:
        x = 1
        for n in range(len(list)):
            songnames = repr(list[n]['title']).replace("'", '')
            singers = list[n]['singer']
            if (len(singers) == 1):
                singername = singers[0].get('name')
            else:
                singername = ''
                for a in singers:
                    medium = '/'
                    singername += a.get('name') + medium
                singername = singername[:-1]
            print(str(x) + '.' + songnames + '-' + singername)
            x += 1
        z = int(input('请输入序号：'))
        z = z - 1
        res = list[z]
        return res
        # print(filename)
        # print(mid)
    except:
        print('获取列表失败！')


# 分离需要的文件信息
def getName(list):
    try:
        mid = list.get('mid')
        songname = list.get('title').replace("'", '')
        singer = list.get('singer')
        if (len(singer) == 1):
            sing = singer[0].get('name')
        else:
            sing = ''
            for b in singer:
                bb = '/'
                sing += b.get('name') + bb
            sing = sing[:-1]
        filename = songname + '-' + sing
        return mid, filename
    except:
        print('获取文件信息！')


#从getName中获取的信息进行下载请求，并保存到本地文件
def getFile(mid, Filename):
    try:
        url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&uin=0&songmid=' + mid + '&filename=C400' + mid + '.m4a&guid=7861126080'
        res = request.urlopen(url).read()
        res = json.loads(res).get('data').get('items')
        songmid = res[0].get('songmid')
        filename = res[0].get('filename')
        vkey = res[0].get('vkey')
        fileurl = 'http://dl.stream.qqmusic.qq.com/' + filename + '?vkey=' + vkey + '&guid=7861126080&uin=0&fromtag=66'
        req = request.urlopen(fileurl).read()
        with open(Filename + '.m4a', 'wb') as outfile:
            outfile.write(req)
        if os.access((Filename + '.m4a'), os.F_OK):
            print('Download File Success!')
        else:
            print('Download File Failure!')
    except:
        print('获取文件失败！')


if __name__ == '__main__':
    data = PrintList(getSongList(input('请输入要搜索歌曲的名字：')))
    res = getName(data)
    Mid = res[0]
    Filename = res[1]
    getFile(Mid, Filename)
