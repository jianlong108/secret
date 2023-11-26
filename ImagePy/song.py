import asyncio
import hashlib
import json
import os.path
import re
import time

import aiofiles
import aiohttp

aaa = input("输入你要爬取的歌曲或歌手（VIP音乐可能只能爬到1分钟）：")

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/89.0.4389.114 Mobile Safari/537.36 "
}


async def main(searchKeyWord, page='1'):
    async with aiohttp.ClientSession() as session:
        url = 'https://complexsearch.kugou.com/v2/search/song'
        t = time.time()
        params = {
            'callback': 'callback123',
            'page': page,
            'keyword': searchKeyWord,
            'pagesize': '30',
            'bitrate': '0',
            'isfuzzy': '0',
            'inputtype': '0',
            'platform': 'WebFilter',
            'userid': '0',
            'clientver': '2000',
            'iscorrection': '1',
            'privilege_filter': '0',
            'token': '',
            'srcappid': '2919',
            'clienttime': str(t),
            'mid': str(t),
            'uuid': str(t),
            'dfid': '-'
        }
        sign_params = ['NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt', 'bitrate=0', 'callback=callback123',
                       'clienttime=' + str(t), 'clientver=2000', 'dfid=-', 'inputtype=0', 'iscorrection=1',
                       'isfuzzy=0',
                       'keyword=' + searchKeyWord, 'mid=' + str(t), 'page=' + page, 'pagesize=30',
                       'platform=WebFilter', 'privilege_filter=0', 'srcappid=2919', 'token=', 'userid=0',
                       'uuid=' + str(t), 'NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt']
        sign_params = ''.join(sign_params)
        signature = hashlib.md5(sign_params.encode(encoding='UTF-8')).hexdigest()
        params['signature'] = signature
        async with session.get(url=url, headers=headers, params=params) as resp:
            if resp.status == 200:
                resp_text = await resp.text()
                json_data = json.loads(resp_text[12:-2:])
                status = json_data['status']
                song_list = []
                if status == 1:
                    for item in json_data['data']['lists']:
                        song_info = {'SongName': re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", item['SongName']),
                                     'AlbumID': item['AlbumID'],
                                     'FileHash': item['FileHash'], 'SQFileHash': item['SQFileHash'],
                                     'HQFileHash': item['HQFileHash'], 'MvHash': item['MvHash'],
                                     'Audioid': item['Audioid'],
                                     'SingerName': re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", item['SingerName'])}
                        song_list.append(song_info)
                else:
                    print(f'获取歌曲列表失败: {json_data["error_msg"]}')
                tasks = []
                if len(song_list) > 0:
                    print(f'获取歌曲列表成功，准备下载...')
                    for song in song_list:
                        task = asyncio.create_task(getSongPlayAddr(song))
                        tasks.append(task)
                await asyncio.wait(tasks)
            else:
                print('连接错误稍后重试')


async def getSongPlayAddr(song_info):
    async with aiohttp.ClientSession() as session:
        url = 'https://wwwapi.kugou.com/yy/index.php'
        params = {
            'r': 'play/getdata',
            'callback': 'jQuery191035601158181920933_1653052693184',
            'hash': song_info['FileHash'],
            'dfid': '2mSZvv2GejpK2VDsgh0K7U0O',
            'appid': '1014',
            'mid': 'c18aeb062e34929c6e90e3af8f7e2512',
            'platid': '4',
            'album_id': song_info['AlbumID'],
            '_': '1653050047389'
        }
        async with session.get(url=url, headers=headers, params=params) as resp:
            if resp.status == 200:
                resp_text = await resp.text()
                json_data = json.loads(resp_text[42:-2:].replace('\\', '').encode('utf8').decode('unicode_escape'))
                await saveMp3(json_data['data']['play_url'], song_info['SongName'], song_info['SingerName'])
            else:
                print('请稍后再试')


async def saveMp3(url, song_name, singer_name):
    if not os.path.exists('../../../../Downloads/课堂资料/爬取歌曲/这个文件夹可以使用  爬取音乐 /music'):
        os.mkdir('../../../../Downloads/课堂资料/爬取歌曲/这个文件夹可以使用  爬取音乐 /music')
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            async with aiofiles.open(f'music/{song_name}-{singer_name}.mp3', mode='wb') as f:
                await f.write(await resp.content.read())
                print(f'{song_name}--{singer_name}--下载完成')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # 默认下载搜索列表的 第一页 共30首
    loop.run_until_complete(main(f'{aaa}'))
