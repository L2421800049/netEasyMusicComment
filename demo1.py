import json

import execjs
import os

import requests


class NetEasyMusicComent:
    def __init__(self,id_):
        with open("./demo.js" , "r" , encoding="utf-8") as f:
            self.ctx = execjs.compile(f.read())
        self.maxPage = 1000
        self.id = id_
        self.info = {
            'rid': 'R_SO_4_{}'.format(self.id),
            'threadId': 'R_SO_4_{}'.format(self.id),
            'pageNo': '1',
            'pageSize': self.maxPage, # 一次评论数 ，测试最大为1000
            'cursor': '-1',
            'offset': '0',
            'orderType': '1',
            'csrf_token': ''
        }

    # 获取post传过去的加密参数
    def getInfo(self):
        res = self.ctx.call("get",json.dumps(self.info))
        res['params'] = res['encText']
        del res['encText']
        return res

    def comment(self):
        url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
        # 当前页
        page = 1

        while True:
            data = self.getInfo()
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
                "content-type": "application/x-www-form-urlencoded",
            }
            res = requests.post(url=url,headers=headers,data=data)
            print("="*50)
            # raise Exception("end")
            try:
                for each in res.json()['data']['comments']:
                    print(each['user']['nickname'] + "  :  " + each['content'])
                    # exit(0)
            except Exception as e:
                print(str(e))
            # 他不是根据pagenum定位下一与 而是返回的cursor
            self.info['cursor'] = res.json()['data']['cursor']
            page += 1

            # 当前页大于最大页码
            if page >= (int(res.json()['data']['totalCount'] / self.maxPage)) + 1:
                exit(0)

    def lyric(self,):
        info = {
            'id': self.id,
            'lv': -1,
            'tv': -1,
            'csrf_token': ''
        }
        # self.info = json.dumps(info)
        # print(self.info)
        res = self.getInfo()
        print(res)
        resp = requests.post(
            url='https://music.163.com/weapi/song/lyric?csrf_token=',
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55" ,
                "content-type": "application/x-www-form-urlencoded",
                # "referer": "https://music.163.com/song?id=%s"%self.id,
                # "origin": "https://music.163.com",
                # "accept": "*/*",
                # "accept-encoding": "gzip, deflate, br",
                # "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            },
            data=res
        )
        print(resp.status_code)
        print(resp.text)

    def main(self):
       self.comment()


if __name__ == '__main__':
    # 这儿是nodejs的地方
    os.environ['NODE_PATH'] = r"D:\nodejs\node_modules\npm\node_modules"
    # 传入歌曲id
    n = NetEasyMusicComent('31877628')
    n.main()