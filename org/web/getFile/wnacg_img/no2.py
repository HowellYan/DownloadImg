# # encoding:utf-8
import requests
import os
import time
import uuid
import urllib2
import cookielib
import re

def get_local_file_exists_size(local_path):
    try:
        lsize = os.stat(local_path).st_size
    except:
        lsize = 0
    return lsize


def get_file_obj(down_link, offset):
    webPage = None
    try:
        headers = {'Range': 'bytes=%d-' % offset}
        webPage = requests.get(down_link, stream=True, headers=headers, timeout=120, verify=False)
        status_code = webPage.status_code
        if status_code in [200, 206]:
            webPage = webPage
        elif status_code == 416:
            print u"%s文件数据请求区间错误,status_code:%s" % (down_link, status_code)
        else:
            print u"%s链接有误,status_code:%s" % (down_link, status_code)
    except Exception as e:
        print u"无法链接:%s,e:%s" % (down_link, e)
    finally:
        return webPage


#获取文件后缀名
def get_file_extension(file):
    return os.path.splitext(file)[1]


#創建文件目录，并返回该目录
def mkdir(path):
    # 去除左右两边的空格
    path = path.strip()
    # 去除尾部 \符号
    path = path.rstrip("\\")

    if not os.path.exists(path):
        os.makedirs(path)

    return path


#'''自动生成一个唯一的字符串，固定长度为36'''
def unique_str():
    return str(uuid.uuid1())


# down_link = 'http://wnacg.download/down/0001/67dd670f043183f0813716dd5f071089.zip'  # 下载链接
# file_size = 271768736  # 文件总大小
# local_path = "/Users/howell/Work/imgscloud/1.zip"

def download_file(down_link, file_size, local_path):
    while True:
        lsize = get_local_file_exists_size(local_path)
        if lsize == file_size:
            break
        webPage = get_file_obj(down_link, lsize)
        try:
            file_obj = open(local_path, 'ab+')
        except Exception as e:
            print u"打开文件:%s失败" % local_path
            break
        try:
            for chunk in webPage.iter_content(chunk_size=64 * 1024):
                if chunk:
                    file_obj.write(chunk)
                else:
                    break
        except Exception as e:
            time.sleep(5)
        file_obj.close()
        webPage.close()

#'''抓取网页文件内容，保存到内存@url 欲抓取文件 ，path+filename'''
def get_file(url, fileCount):
    try:
        cj = cookielib.LWPCookieJar()
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        req = urllib2.Request(url,  headers=hdr)
        operate = opener.open(req)
        data = operate.read()
        res_tr = r'<a class="down_btn" href="(.*?)" target="_blank">'
        url = re.findall(res_tr, str(data), re.S | re.M)[0]

        print url
        f = urllib2.urlopen(url)
        meta = f.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        content_type = meta.getheaders('Content-Type')[0].split(';')[0]
        print file_size, content_type
        download_file(url, file_size, "/Users/howell/Work/imgscloud/"+str(fileCount)+".zip")
        # data = f.read()
        # with open("/Users/howell/Work/imgscloud/"+str(fileCount)+".zip", "wb") as code:
        #     code.write(data)

        return data
    except BaseException, e:
        print e
        return None


'''
保存文件到本地
@path  本地路径
@file_name 文件名
@data 文件内容
'''


def save_file(path, file_name, data):
    if data == None:
        return

    mkdir(path)
    if (not path.endswith("/")):
        path = path + "/"
    file = open(path + file_name, "wb")
    file.write(data)
    file.flush()
    file.close()


# 获取文件后缀名
# print get_file_extension("123.jpg")

# 創建文件目录，并返回该目录
# print mkdir("/Users/howell/Work/ljq")

# 自动生成一个唯一的字符串，固定长度为36
# print unique_str()

# 7370
fileCount=1
while fileCount <= 3:

    url = "https://www.wnacg.com/download-index-aid-"+str(fileCount)+".html"
    print url
    data = get_file(url,fileCount)
    if data == None:
        fileCount -= 1
        count = 0
    save_file("/Users/howell/Work/imgscloud/"+str(fileCount), str(fileCount)+".html", data)

    fileCount+=1

