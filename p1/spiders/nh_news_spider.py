import scrapy
from bs4 import BeautifulSoup
import urllib2

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo
from pymongo import MongoClient


client = MongoClient(host="59.110.157.232", port=27017)

db = client.news;

collection = db.news


class MsxwSpider(scrapy.Spider):
    name = "nhnews"
    allowed_domains = ["nhnews.org"]
    domain = 'http://nh.cnnb.com.cn'
    count = 0
    start_urls = [
        "http://nh.cnnb.com.cn/news/nhnews",
        "http://nh.cnnb.com.cn/news/msxw",
        "http://nh.cnnb.com.cn/news/waimei"
    ]

    def get_content(self,url):

        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

        headers = {'User-Agent': user_agent}

        request = urllib2.Request(url,headers=headers)

        response = urllib2.urlopen(request)

        body = response.read()

        soup = BeautifulSoup(body,'lxml',from_encoding="utf-8")

        soup.encoding = 'utf-8'

        content = [];

        for p in soup.select(".topic")[0].select('p'):

            content.append(p.text)

        return content


    def parse(self, response):

        soup = BeautifulSoup(response.body,'lxml',from_encoding="utf-8");
        soup.encoding = 'utf-8'

        for list in soup.select("#Columns")[0].select('li'):

            new_time = list.span.text

            link = list.a['href'];

            title = list.a.text;

            content = self.get_content(self.domain+link);

            content_str = "";

            for str in content:
                content_str+=str


            jason = {

                 'title':title,
                 'content':content_str,
                 'new_time':new_time,
                  'orign':response.url
             }

            collection.insert(jason)