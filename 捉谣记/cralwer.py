# -*- coding: utf-8 -*-
import requests, json, os,sys
import urllib.parse
root_path = os.path.split(sys.path[0])[0]

def get_url(ptime=0,default_error_time=0):
    url = r'https://piyao.sina.cn/api/list/group'
    data = {
        'len': 20,
        'ptime': ptime
    }
    try:
        response = requests.get(url,params = data,timeout=3)
        return response.text
    except Exception as e:
        print(e)
        if default_error_time > 3:
            return "ERROR RESPONSE"
        get_url(ptime,default_error_time+1)


if __name__ == '__main__':

    current_date = '2020-05-11'
    current_ptime = 0
    article_list = []
    while current_date > '2019-09-01':
        result = get_url(ptime=current_ptime)
        data = json.loads(urllib.parse.unquote(result))['result']['data']
        for date in data.keys():
            current_date = date
            for i in data[date]:
                article = {
                    'id':i['id'],
                    "article_id":i['article_id'],
                    "column_id":i['column_id'],
                    "author":i['author'],
                    "ctime":i['ctime'],
                    "mtime":i['mtime'],
                    "ptime":i['ptime'],
                    "audit":i['audit'],
                    "creator":i['creator'],
                    "mender":i['mender'],
                    "title":i['title'],
                    "stitle":i['stitle'],
                    "tags":i['tags'],
                    "level":i['level'],
                    "url":i['url'],
                    'date':date
                }
                article_list.append(article)
                current_ptime = i['ptime']
    with open(root_path+'/sourse_data/zhuoyaoji.json','w',encoding='utf-8') as f:
        f.write(json.dumps(article_list))
