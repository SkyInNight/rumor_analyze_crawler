#-*- coding: utf-8 -*-
import requests, json, os,sys
import urllib.parse


root_path = os.path.split(sys.path[0])[0]

def get_url(pgnum,default_error_time=0):
    url = r'https://feed.mix.sina.com.cn/api/roll/get'
    data = {
        'pageid': 153,
        'lid': 2509,
        'num': 50,
        'page': pgnum
    }
    try:
        response = requests.get(url,params = data,timeout=3)
        return response.text
    except Exception as e:
        print(e)
        if default_error_time > 3:
            return "ERROR RESPONSE"
        get_url(pgnum,default_error_time+1)

def data_parser(text):
    # text = text[1:-1]
    json_data  = json.loads(text)
    return json_data

if __name__ == '__main__':
    # current_date = '2020-05-11'
    pgnum = 1
    article_list = []
    while pgnum < 50:
        result = get_url(pgnum)
        data_list = data_parser(urllib.parse.unquote(result))['result']['data']
        for data in data_list:
            article = {
                'docid':data['docid'],
                'url':data['url'],
                'wapurl':data['wapurl'],
                'title':data['title'],
                'intro':data['intro'],
                'ctime':data['ctime'],
                'mtime':data['mtime'],
                'intime':data['intime'],
                'keywords':data['keywords'],
                'date':data['url'].split('/')[-2]
                }
            article_list.append(article)
        pgnum+=1
    with open(root_path+'/sourse_data/xinlangxinwen.json','w',encoding='utf-8') as f:
        f.write(json.dumps(article_list))
