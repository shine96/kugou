import json
import os
import requests
from urllib import parse


# 获取搜索歌曲列表
def getSongList(keyword):
    try:
        url = "http://songsearch.kugou.com/song_search_v2?keyword="
        url_data = "&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1489023388641"
        res = requests.get(url+keyword+url_data).text
        res = json.loads(res)
        res = res['data']['lists']
        return res
    except:
        print('列表搜索失败！')


# 打印输出列表，并等待客户输入选择
def getSongHash(List):
    try:
        x = 1
        for n in range(len(List)):
            name = repr(List[n]['FileName'])
            name = name.replace('<em>', '').replace('</em>', '').replace("'", '')
            print(str(x) + '.' + name)
            x += 1
        z = input('请输入需要下载歌曲的序号：')
        if (z == '0'):
            return '0'
        elif (z == ''):
            return 'null'
        else:
            z = int(z)
            z -= 1
            filename = List[z]['FileName'].replace('<em>', '').replace('</em>', '')
            filehash = List[z]['FileHash']
            return filehash, filename
    except:
        print('搜索失败！')


# 得到歌曲的下载地址
def getDownUrl(hash):
    try:
        song_url = "https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash="+ hash+"&album_id=20119567&dfid=1HZv9x1cdITX0MrhHt0rvqjX&mid=8072781460320aa18e05e7110632723b&platid=4&_=1562462788383"
        song_res = requests.get(song_url).text
        song_res = json.loads(song_res)
        DownUrl = song_res['data']['play_url']
        return DownUrl
    except:
        print("获取下载链接失败！")

# 下载歌曲文件
def DownFile(DownUrl, new_name):
    try:
        file = requests.get(DownUrl).content
        with open(new_name + '.mp3', 'wb') as outfile:
            outfile.write(file)
    except:
        print('本地文件写入失败！')

def main():
    try:
        keyword = parse.quote(input("请输入需要搜索歌曲名字:"))
        list = getSongList(keyword)
        data = getSongHash(list)
        if (data == '0'):
            ins = input('是否要退出程序（Y/N）？')
            if (ins == 'y' or ins == 'Y'):
                print('Good Bye!')
                exit()
            else:
                main()
        elif (data == 'null'):
            print('输入有误请重新输入')
            main()
        else:
            DownFile(getDownUrl(data[0]), data[1])
            if os.access((data[1] + '.mp3'), os.F_OK):
                print('Download File Success!')
            else:
                print('Download File Failure!')
            print(input('请按任意键退出程序！'))
    except:
        print('程序异常！')


if __name__ == '__main__':
    main()
