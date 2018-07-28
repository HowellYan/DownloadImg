# -* - coding: UTF-8 -* -
from HTMLParser import HTMLParser
import htmllib, urllib, formatter, string
import os, sys, time
import threading



# 建立线程池，并启动线程直到结束
def parallel(urls):
    startTime = time.time()
    threads = []
    counts = range(len(urls))
    for i in counts:
        t = MyThread(downloadFromURL, (urls[i],), downloadFromURL.__name__)
        threads.append(t)
    for i in counts:
        threads[i].start()
    for i in counts:
        threads[i].join()
    print 'use time cost:%s' % (time.time() - startTime)


# 自定义线程类
class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        apply(self.func, self.args)

        # 根据url找到图片的链接并下载


def downloadFromURL(url):
    fp = urllib.urlopen(url)
    data = fp.read()
    fp.close()

    hp = MyHTMLParser()
    hp.feed(data)
    hp.close()
    for i in hp.links:
        print(i)
        downloadImage(i)

        # 根绝imageUrl下载图片到本地


def downloadImage(imageUrl):
    dir = "./image_douban"
    try:
        if not os.path.exists(dir):
            os.mkdir(dir)
    except:
        print "Failed to create directory in %s" % dir
        exit()
    image = imageUrl.split('/')[-1]
    path = dir + "/" + image
    data = urllib.urlopen(imageUrl).read()
    f = file(path, "wb")
    f.write(data)
    f.close()


# 定义html解析，关键在于handle_starttag
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if len(attrs) == 0:
            pass
        else:
            for (variable, value) in attrs:
                if variable == "src" and value[:4] == "http" and value[-4:] == ".jpg":
                    self.links.append(value)


if __name__ == "__main__":
    html = """
    <a href="www.google.com"> google.com</a>
    <A Href="www.pythonclub.org"> PythonClub </a>
    <A HREF = "www.sina.com.cn"> Sina </a>
    """
    # url2 = "http://image.baidu.com/i?ct=201326592&cl=2&lm=-1&tn=baiduimage&pv=&word=car&z=5"
    # url = "http://image.baidu.com"
    # url = "http://movie.douban.com/"
    # 下载豆瓣电影图片
    base = 20
    count = 1
    urls = []
    while count <= 100:
        url = "http://movie.douban.com/tag/%E6%83%8A%E6%82%9A?start=" + str(base * count) + "&type=T"
        urls.append(url)
        count += 1
    parallel(urls)