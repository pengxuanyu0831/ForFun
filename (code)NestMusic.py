#__author__=penxy
#-*- coding:utf-8-*-

from bs4 import BeautifulSoup
import re
import time
import requests
from lxml import etree
from selenium import webdriver
import random
import json
import logging
import os,sys




class music163_spider:
    # 初始化数据
    def __init__(self):
    #def __init__(self,logname,fmt='%(asctime)s %(pathname)s %(logname)s %(levelname)s: %(msg)s'):
        opt = webdriver.chrome.options.Options()
        opt.set_headless()
        self.brower = webdriver.Chrome(chrome_options=opt)
        self.originURL = 'https://music.163.com/#/discover/playlist'
        self.data = list()
        #self.logger = logging.getLogger(logname)
        #format_str = logging.Formatter(fmt,datefmt="%Y%M%D")
        #self.logger.setLevel(logging.DEBUG)
        #ch = logging.StreamHandler()  # 输出到控制台
        #ch.setFormatter(format_str)   # 输出到控制台的格式
        #fh = logging.FileHandler(logname = logname, encoding='utf-8')  # 写入文件
        #fh.setFormatter(format_str)   # 写入文件的格式
        #self.logger.addHandler(ch)
        #self.logger.addFilter(fh)



#爬取网易云音乐中的高播放量的歌单

    def get_cur_time():
        #Now_time = time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
        #print('歌单更新时间'+Now_time)
        return time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))


    def get_songslist(self,url):
        #header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
              #'referer': 'https://music.163.com/discover/playlist'}

        #response = requests.get(self.originURL,headers = header)
        self.brower.get(url)
        self.brower.switch_to.frame('g_iframe')
        html = self.brower.page_source
        return html


    def info_songslist(self,html):
        html_elem = etree.HTML(html)
        play_number = html_elem.xpath('//ul[@id="m-pl-container"]/li/div/div/span[@class="nb"]/text()')
        #                              //*[@id="m-pl-container"]/li[1]/div/div/span[2]
        song_list_title = html_elem.xpath('//ul[@id="m-pl-container"]/li/p[1]/a/@title')
        song_list_url = html_elem.xpath('//ul[@id="m-pl-container"]/li/p[1]/a/@href')
        song_url = ('https://music.163.com/#'+ item for item in song_list_url)
        data = list(map(lambda a,b,c,d:{'播放量':a,'歌单名称':b,'歌单链接':c,'歌曲链接':d},
                        play_number,song_list_title,song_list_url,song_url))
        return data


    def next_page_link(self,html):
        html_elem = etree.HTML(html)
        next_page_link = html_elem.xpath('//div[@id="m-pl-pager"]/div[@class="u-page"]/a[@class="zbtn znxt"]/@href')
        if not next_page_link:
            return None
        else:
            return 'https://music.163.com/#' + next_page_link[0]

    #获取当前环境的桌面路径
    #def get_desktop_path(self):运行报错:"Permission denied"，尚未想到好的解决办法，只好将保存路径设置在非系统盘下
        #key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        #return winreg.QueryValueEx(key, "Desktop")[0]


    def spider_begin(self,path):
        #path = str(spider.get_desktop_path())
        #logger.info("爬取歌单列表:" + path)
        Now_time = time.strftime('%Y.%m.%d %H_%M_%S', time.localtime(time.time()))
        print('歌单获取时间：'+ Now_time)
        time.sleep(2)
        print('开始爬取。')
        time.sleep(2)
        print('正在爬取...')

        html = self.get_songslist(self.originURL)
        data = self.info_songslist(html)
        self.data.extend(data)
        link = self.next_page_link(html)
        #index = 1
        #number = self.play_number(data)
        while(link):
            html = self.get_songslist(link)
            data = self.info_songslist(html)
            self.data.extend(data)
            link = self.next_page_link(html)
            #number = self.play_number(data)
            time.sleep(random.random())
        print('数据处理中...')
        time.sleep(3)
        #按播放量排序
        data_after_sort = sorted(self.data,key = lambda item:int(item['播放量'].replace('万','0000')),reverse = True)
        print('写入文件中...')
        time.sleep(5)
        filename = 'D:/'+ Now_time+ r'_163musiclist.json'#这里有个点需要注意，保存时文件名中不允许出现: 所以Now_time定义时如果用了: 在这里需要回去改掉，改成下划线
        with open(filename,'w+',encoding='utf-8') as f:
            #f.write(data.encode('utf-8'))
            #f.write(data)
            for item in data_after_sort:
                #json.dump(item,f,ensure_ascii = False)
                json.dump(item,f,ensure_ascii=False,indent=4)   #indent = 4 是dump参数之一，用处是数据格式缩进显示
                #json.write(str(item)+'\n',f, ensure_ascii=False)
                #for file in item:
                    #data.append('\n' + json.loads(str(item)))




    def write_result(self,str):
        Now_time = time.strftime('%Y.%m.%d %H_%M_%S', time.localtime(time.time()))
        filename = 'D:/'+ Now_time+ r'_163musiclist.json'
        write_result = filename
        str1 = write_result.write(str + '\n')
        write_result.close()
        return str



'''
    def get_logger(log_dir):
        fh = logging.FileHandler(log_dir, encoding='utf-8', mode='w')
        sh = logging.StreamHandler()
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        fm = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        logger.addHandler(fh)
        logger.addHandler(sh)
        fh.setFormatter(fm)
        sh.setFormatter(fm)
        return logger




    def logging(self,logname,msg):
        Now_time = time.strftime('%Y.%m.%d %H_%M_%S', time.localtime(time.time()))
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        logname = 'D:/' + Now_time + r'_163muscilistlog.txt'
        fh = logging.FileHandler(logname,encoding='utf-8')#写入文件
        ch = logging.StreamHandler(logname)#输出到控制台
        formatter = logging.Formatter(
            fmt= "%(asctime)s %(name)s %(logname)s %(msg)s",
            datefmt = "%Y%M%D"
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        self.logger.info(msg)
'''


if __name__ == '__main__':
    spider = music163_spider()
    #write = write_result()
    path = 'D://'
    #path = str(spider.get_desktop_path()) #调用之前要先实例化
    spider.spider_begin(path)
    print('爬取完成!')
    print('爬取完成的歌单保存在:' + path)
    #差一个日志输出部分














'''
import requests
import re
import time
from bs4 import BeautifulSoup

cat ='2'
img = 'https://www.dbmeinv.com/index.htm?cid='+ cat
#https://www.dbmeinv.com/index.htm?cid=2
end = '/dbgroup/show.htm?cid='+ cat + '&pager_offset=100'
urls = [ ]
def getURLs(mainURL):
    time.sleep(1)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    html = requests.get(mainURL).text
    soup = BeautifulSoup(html, 'html.parser')
    picURL = re.findall('<img class.*?src="(.+?\.jpg)"', html, re.S)
    #n = 0
    for url in picURL:
        urls.append(url)
        print(url)
        if urls.__len__() > 6:
            return urls
    asoup = soup.select('.next a')[0]['href']
    Next_page = 'http://www.dbmeinv.com' + asoup
    if asoup != end:
        getURLs(Next_page)
    else:
        print('链接已处理完毕！')
    return urls
url = getURLs(img)

i = 0
for each in url:
    pic = requests.get(each, timeout = 10)
    picName = 'pictures/' + str(i) + '.jpg'
   # fp = u"Picname"
    fp = open(u"Picname", 'w')
    print(pic.content)
    fp.write(pic.content)
    fp.close()
    i += 1

print('图片下载完成')
'''





