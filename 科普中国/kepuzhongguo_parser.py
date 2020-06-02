# encoding:utf-8
from html_parser import HtmlParserInterface
import re
from bs4 import BeautifulSoup
import json


class FoodParser(HtmlParserInterface):
    def parser(self,context):
        soup = BeautifulSoup(context,'lxml')
        a_list = soup.select("div.layoutContent > div >div.dialog-list > div > div.txt > h2 > a")
        url_list = []
        for a in a_list:
            # url_list.append(json.dumps({'title':a.string, 'href':a['href']}))
            url_list.append(a.get_text())
        return url_list

class KepuzhongguoParser(HtmlParserInterface):

    def pagenum_parser(self, context):
        regex = re.compile(r'<div class="total-page">共(\d+)页</div>',re.I)
        page_num = regex.findall(context)[0]
        return page_num

    def parser(self,context):
        # <a.*?href=(".*?").*?>.+?</a>.*?
        soup = BeautifulSoup(context,'lxml')
        # a_list = soup.select("div.rumor-data-list > ul > li > a")
        li_list = soup.select("div.main>div>div.rumor-data-list>ul>li")
        url_list = []
        for li in li_list:
            span = li.select('div.expert-msg > span')[1].text.split(' ')[0]
            if span < "2020-04-01":
                continue
            a = li.select('a')[0]
            # url_list.append(json.dumps({'title':a.string, 'href':a['href']}))
            url_list.append(a['href'])
        return url_list

class ContentParser(HtmlParserInterface):
    def parser(self,context):
        soup = BeautifulSoup(context,'lxml')
        title_list = soup.select('div.main.list-detail > div.content > h2')
        title = title_list[0].contents[0].strip()
        title = re.sub('[\/:*?"<>|]','-',title)
        content = soup.find('div',class_ = 'content').prettify()
        result = json.dumps({'title':title,'content':content})
        return result

class TitleParser(HtmlParserInterface):
    def parser(self,context):
        soup = BeautifulSoup(context,'lxml')
        title_list = soup.select('div.main.list-detail > div.content > h2')
        title = title_list[0].contents[0].strip()
        return title