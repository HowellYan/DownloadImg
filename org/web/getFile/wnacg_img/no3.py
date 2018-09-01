# # encoding:utf-8
import requests
import os
import time
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


def save_file(down_link, file_size, local_path):
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
            time.sleep(1)
        file_obj.close()
        webPage.close()


#創建文件目录，并返回该目录
def mkdir(path):
    # 去除左右两边的空格
    path = path.strip()
    # 去除尾部 \符号
    path = path.rstrip("\\")

    if not os.path.exists(path):
        os.makedirs(path)

    return path

def save_html(path, file_name, data):
    if data == None:
        return

    mkdir(path)
    if (not path.endswith("/")):
        path = path + "/"
    file = open(path + file_name, "wb")
    file.write(data)
    file.flush()
    file.close()


#'''抓取网页文件内容，保存到内存@url 欲抓取文件 ，path+filename'''
def get_file(url):
    try:
        cj = cookielib.LWPCookieJar()
        hdr = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'cookie': '__cfduid=dbe3e3ab1f371e507ebec44a0b19787d61532949384; cf_clearance=a17376b236768f65bf4af49bdea397dd49ca261b-1534821176-604800-250',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        req = urllib2.Request(url,  headers=hdr)
        operate = opener.open(req)
        data = operate.read()
        return data
    except BaseException, e:
        print str(e)
        return None


fileCount=54574
while fileCount >= 206:


    url = "https://www.wnacg.com/download-index-aid-"+str(fileCount)+".html"
    print url
    data = get_file(url)

    res_tr = r'<a class="down_btn" href="(.*?)" target="_blank">'
    down_link = re.findall(res_tr, str(data), re.S | re.M)[0]

    es_tr = r'<p class="download_filename">(.*?)</p>'
    name_file = re.findall(es_tr, str(data), re.S | re.M)[0]

    if data == None:
        fileCount -= 1
        count = 0
    save_html("/Users/howell/Work/imgscloud/"+str(fileCount), str(fileCount)+".html", data)

    print down_link
    if(".zip" == name_file):
        fileCount -= 1
    else:
        # down_link = 'http://wnacg.download/down/0001/67dd670f043183f0813716dd5f071089.zip'  # 下载链接
        local_path = "/Users/howell/Work/imgscloud/"+str(fileCount)+".zip"

        try:
            file = urllib2.urlopen(down_link)
            meta = file.info()
            file_size = int(meta.getheaders("Content-Length")[0])  # 文件总大小
            content_type = meta.getheaders('Content-Type')[0].split(';')[0]
            print file_size, content_type, local_path, local_path, down_link

            save_file(down_link, file_size, local_path)

        except urllib2.HTTPError, err:
            print err.code

        except urllib2.URLError, err:
            print err

        fileCount-=1



