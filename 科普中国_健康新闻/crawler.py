#-*- coding: utf-8 -*-
import requests, json, os,sys
import urllib.parse
from bs4 import BeautifulSoup


root_path = os.path.split(sys.path[0])[0]

def get_url(pgnum,default_error_time=0):
    url = r'https://www.kepuchina.cn/health/index'
    if pgnum == 1:
        url += ".shtml"
    else:
        url += "_" + str(pgnum-1) + ".shtml"
    try:
        response = requests.get(url,timeout=3)
        return response.content.decode('utf-8')
    except Exception as e:
        print(e)
        if default_error_time > 3:
            return "ERROR RESPONSE"
        get_url(pgnum,default_error_time+1)


def data_parser(text):
    # text = urllib.parse.unquote(text)
    soup = BeautifulSoup(text,'lxml')
    div_list = soup.select('div.content > div.layout-right-cont > div > div > div > div > div')
    title_list = []
    for div in div_list:
        data = div.select('p > em')[0].text
        if data < '2020-04-01':
            continue
        a = div.select('h2 > a')[0]
        title_list.append(a.string)
    return title_list

if __name__ == '__main__':
    # result = get_url(pgnum=1)
    title_list = []
    for i in range(1,35):
        result = get_url(pgnum=i)
        data_list = data_parser(result)
        for data in data_list:
            title_list.append(data)
    # print(data_parser(result))
    # totalnum = data_parser(result)['totalnum']
    # nid = 11215616
    # article_list = []
    # for i in range(1,6):
    #     result = get_url(nid=nid,pgnum=i,cnt=totalnum)
    #     data_list = data_parser(urllib.parse.unquote(result))['data']['list']
    #     for data in data_list:
    #         article = {
    #             'DocID':data['DocID'],
    #             'Title':data['Title'],
    #             'NodeId':data['NodeId'],
    #             'PubTime':data['PubTime'],
    #             'LinkUrl':data['LinkUrl'],
    #             'keyword':data['keyword'],
    #             'Editor':data['Editor'],
    #             'Author':data['Author'],
    #             'SourceName':data['SourceName'],
    #             'IsLink':data['IsLink']
    #             }
    #         nid = data['NodeId']
    #         article_list.append(article)
    with open(root_path+'/sourse_data/kepuzhongguoxinwen.txt','w',encoding='utf-8') as f:
        for title in title_list:
            f.write(title+'\n')