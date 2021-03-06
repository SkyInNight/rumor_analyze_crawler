#-*- coding: utf-8 -*-
import requests, json, os,sys
import urllib.parse

root_path = os.path.split(sys.path[0])[0]

def get_url(nid,pgnum,cnt,default_error_time=0):
    url = r'http://qc.wa.news.cn/nodeart/list'
    data = {
        'nid': nid,
        'pgnum': pgnum,
        'cnt': cnt
    }
    try:
        response = requests.get(url,params = data,timeout=3)
        return response.text
    except Exception as e:
        print(e)
        if default_error_time > 3:
            return "ERROR RESPONSE"
        get_url(nid,pgnum,cnt,default_error_time+1)


def data_parser(text):
    text = text[1:-1]
    json_data  = json.loads(text)
    return json_data

if __name__ == '__main__':
    result = get_url(nid=11215616,pgnum=1,cnt=1)
    totalnum = data_parser(result)['totalnum']
    nid = 11215616
    article_list = []
    for i in range(1,6):
        result = get_url(nid=nid,pgnum=i,cnt=totalnum)
        data_list = data_parser(urllib.parse.unquote(result))['data']['list']
        for data in data_list:
            article = {
                'DocID':data['DocID'],
                'Title':data['Title'],
                'NodeId':data['NodeId'],
                'PubTime':data['PubTime'],
                'LinkUrl':data['LinkUrl'],
                'keyword':data['keyword'],
                'Editor':data['Editor'],
                'Author':data['Author'],
                'SourceName':data['SourceName'],
                'IsLink':data['IsLink']
                }
            nid = data['NodeId']
            article_list.append(article)
    with open(root_path+'/sourse_data/piyao_xinguanzhuanqu.json','w',encoding='utf-8') as f:
        f.write(json.dumps(article_list))