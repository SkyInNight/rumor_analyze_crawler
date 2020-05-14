import selenium
from selenium import webdriver #测试框架模拟浏览器# 创建chrome参数对象
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import os,sys,json

root_path = os.path.split(sys.path[0])[0]


def get_driver():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    browser_driver_ = webdriver.Firefox(
        executable_path=root_path + r"/driver/geckodriver.exe",  # 这里必须要是绝对路径
        firefox_binary=r"C:/Program Files/Mozilla Firefox/firefox.exe",
        options=options
    )
    return browser_driver_



def get_url(driver, pgnum=1,default_error_time=0):
    try:
        url = r'http://www.nhc.gov.cn/xcs/xwbd/list_gzbd'
        if pgnum == 1:
            url += '.shtml'
        else:
            url+='_'+str(pgnum)+'.shtml'
        driver.get(url)
        print('current url is '+driver.current_url)
        # print(driver.page_source)
        return driver.page_source
    except Exception as e:
        print(e)


if __name__ == '__main__':
    driver_ = get_driver()
    article_list = []
    origin_url = r'http://www.nhc.gov.cn/'
    try:
        result = get_url(driver_)
        for page in range(1,35):
            result = get_url(driver_,pgnum=page)
            soup = BeautifulSoup(result, 'lxml')
            li_list = soup.select('div.list > ul.zxxx_list > li')
            for li in li_list:
                url = li.select('a')[0]
                span = li.select('span')[0]
                article = {
                    'url':origin_url+url['href'],
                    'title':url['title'],
                    'date':span.text
                }
                article_list.append(article)
        # print(article_list)
        with open(root_path+'/sourse_data/guojiaweijianwei.json','w',encoding='utf-8') as f:
            f.write(json.dumps(article_list))
    except Exception as e:
        print(e)
    finally:
        driver_.close()