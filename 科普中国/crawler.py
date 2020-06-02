# coding=utf-8
import requests,os,json
from fake_useragent import UserAgent

class CrawlerInterface:

    def crawling(self,url_list,rule_model):
        '''
        - param url：需要爬取的url
        - param rule_model：自定义html解析模型
        返回爬取信息
        '''
    
    def crawling(self,url,rule_model,headers,data):
        '''
        '''

class Crawler(CrawlerInterface):
    
    def crawling_ke(self,url,rule_model,headers,data = ""):
        response = requests.get(url,headers=headers,params=data)
        response.encoding = response.apparent_encoding
        html = response.text
        result = rule_model.parser(context = html)
        return result

    def crawling(self,url_list,rule_model):
        resule_list = []
        for url in url_list:
            ua = UserAgent()
            headers = {
                "Origin":url,
                'User-Agent':ua.random,
                "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                # "Accept-Encoding":"gzip, deflate, br",
                "Content-Type":"text/html; charset=utf-8",
            }
            response = requests.get(url,headers=headers)
            response.encoding = response.apparent_encoding
            html = response.text
            result = rule_model.parser(context = html)
            resule_list.append(result)
        return resule_list



    