# -*-coding:utf-8-*-

import os
import uuid
import urllib2
import cookielib
import re

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
        # res_tr = r'<a class="down_btn" href="(.*?)" target="_blank">'
        # url = re.findall(res_tr, str(data), re.S | re.M)[0]
        #
        # print url
        # f = urllib2.urlopen(url)
        # meta = f.info()
        # file_size = int(meta.getheaders("Content-Length")[0])
        # content_type = meta.getheaders('Content-Type')[0].split(';')[0]
        # print file_size, content_type
        # data = f.read()
        # with open("/Users/howell/Work/imgscloud/"+str(fileCount)+".zip", "wb") as code:
        #     code.write(data)

        return data
    except BaseException, e:
        print e
        return None


def get_file_zip(url, fileCount):
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
print get_file_extension("123.jpg")

# 創建文件目录，并返回该目录
# print mkdir("/Users/howell/Work/ljq")

# 自动生成一个唯一的字符串，固定长度为36
print unique_str()

# 7370
fileCount=1
while fileCount <= 3:

    url = "https://www.wnacg.com/download-index-aid-"+str(fileCount)+".html"
    print url
    data = get_file(url,fileCount)

    res_tr = r'<a class="down_btn" href="(.*?)" target="_blank">'
    url = re.findall(res_tr, str(data), re.S | re.M)[0]

    if data == None:
        fileCount -= 1
        count = 0
    save_file("/Users/howell/Work/imgscloud/"+str(fileCount), str(fileCount)+".html", data)

    print url
    data = get_file_zip(url, fileCount)

    save_file("/Users/howell/Work/imgscloud/"+str(fileCount), str(fileCount)+".zip", data)



    fileCount+=1

