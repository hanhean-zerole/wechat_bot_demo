import threading
import shutil
import os
import re
import wxauto
from General import PIXIV_IMG

import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'referer': 'https://www.pixiv.net/ranking.php?mode=daily&content=illust',
}



def getSinglePic(ID):
    global repeat
    picUrl = 'https://www.pixiv.net/ajax/illust/' + ID + "/pages?lang=zh"
    response = requests.get(picUrl, headers=headers)
    # 提取图片原图地址
    picture = re.search('"original":"(.+?)"},', response.text)
    try:
        pic = requests.get(picture.group(1).replace('\\', ''), headers=headers)
        f = open(PIXIV_IMG + '%s.%s' % (ID, picture.group(1)[-3:]), 'wb')
        f.write(pic.content)
        f.close()
    except :
        print("下载出错,错误URL为" + response.text)

def getAllPic():
    count = 1
    for n in range(1, 10 + 1):
        url = 'https://www.pixiv.net/ranking.php?mode=daily&content=illust&p=%d&format=json' % n
        response = requests.get(url, headers=headers)
        illust_id = re.findall('"illust_id":(\d+?),', response.text)
        for id in illust_id:
            getSinglePic(id)
            count += 1
    return None


def delete_directory_contents(directory):
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"删除 {file_path} 时出错: {e}")

        print(f"已完成清理目录: {directory}")
    except Exception as e:
        print(f"访问目录 {directory} 时出错: {e}")


def download_pixiv_recommend():
    delete_directory_contents(PIXIV_IMG)
    thread_download = threading.Thread(target=getAllPic)
    thread_download.start()
    thread_download.join()


if __name__ == '__main__':
    download_pixiv_recommend()