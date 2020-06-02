#-*- coding: UTF-8 -*-
from crawler import Crawler
from kepuzhongguo_parser import KepuzhongguoParser,TitleParser
import requests
from fake_useragent import UserAgent
from multiprocessing import Process, Pool,freeze_support
import time,os,sys
import multiprocessing

root_path = os.path.split(sys.path[0])[0]
#maxsize=-1:设置队列中嫩够存储的最大元素的个数
# data_queue = Queue(maxsize=50)
def Foo(page_list):
    out = []
    url = 'https://piyao.kepuchina.cn/rumor/rumorlist'
    parser = KepuzhongguoParser()
    title_parser = TitleParser()
    ua = UserAgent()
    headers = {
                "Origin":url,
                'User-Agent':ua.random,
                "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                # "Accept-Encoding":"gzip, deflate, br",
                "Content-Type":"text/html; charset=utf-8",
            }
    crawler = Crawler()
    title_list = []
    for page in page_list:
        data = {'type':0,'keyword':0,'page':page}
        url_list = crawler.crawling_ke(url, rule_model=parser,data=data,headers=headers)
        for url_1 in url_list:
            title = crawler.crawling_ke(url_1, rule_model=title_parser, headers=headers)
            title_list.append(title)
        # out.append(url_list)
    return title_list

def test(page_list):
    return page_list
def callback(arg):
    print(arg)
def Bar(arg):
    # print (arg)
    with open(root_path+'/sourse_data/kepuzhongguo.txt','a+',encoding='utf-8') as out:
        for url_list in arg:
            # for url in url_list:
                out.write(url_list+'\n')


if __name__ == '__main__':
    url = 'https://piyao.kepuchina.cn/rumor/rumorlist'
    parser = KepuzhongguoParser()
    context = requests.get(url).text
    ua = UserAgent()
    page_num = parser.pagenum_parser(context)
    task_list = []
    # print(Foo([1,2]))
    '''
    crawler = Crawler()
    for page in range(1,int(page_num)+1):
        headers = {
                "Origin":url,
                'User-Agent':ua.random,
                "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                # "Accept-Encoding":"gzip, deflate, br",
                "Content-Type":"text/html; charset=utf-8",
            }
        data = {'type':0,'keyword':0,'page':page}
        url_list = crawler.crawling_ke(url=url, rule_model=parser,data=data,headers=headers)
        with open('url.txt','a+',encoding='utf-8') as out:
            for i in url_list:
                out.write(i+'\n')
    #     task_list.append(url_list)

    '''
    pool = multiprocessing.Pool(processes=10)
    for i in range(1,int(page_num)+1,15):
        page_list = []
        for j in range(i,i+35):
            if j > int(page_num):
                break
            page_list.append(j)
        pool.apply_async(func=Foo, args=(page_list,),callback=Bar)
    pool.close()
    pool.join()


    # pool = Pool(4)              #允许进程池里同时放入5个进程，放入进程池里的进程才会运行，其他进程挂起
    '''
    for i in range(1,int(page_num)+1,35):
        input_data = [i:i+35]
        pool.apply_async(func=Foo, args=(input_data,),callback=Bar)
        # pool.apply_async(func=Foo, args=(input_data,), callback=Bar) #并行 ，callback回调 干完foo才能干bar，干不完foo不干bar。  主进程调用的回调。备份完毕自动向数据库写日志。为什么不在子进程写日志？因为父进程只连一次，而子进程要连10次。
    # print('end')
    pool.close()    #一定要先关闭进程池再join
    pool.join()  # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭，不等进程执行完毕程序直接关闭 先close在join
    '''