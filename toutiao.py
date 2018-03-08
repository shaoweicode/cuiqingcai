import requests
import json
from urllib.parse import urlencode
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
# 返回索引页面HTML
def get_page_index(offset,keyword):
    data = {

        'autoload':'true',
        'count':'20',
        'cur_tab':'1',
        'format':'json',
        'from':'search_tab',
        'keyword':keyword,
        'offset':offset
    }
    url = 'https://www.toutiao.com/search_content/?'+urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None
#返回索引页中每个大图页的链接
def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')
# 返回大图页面的html
def get_page_detail(url):
    try:
        data = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:58.0) Gecko/20100101 Firefox/58.0'}
        cookie = {'Cookie':'tt_webid=6530495836253488644; WEATHER_CITY=%E5%8C%97%'}
        response = requests.get(url,data=data,cookies=cookie)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错')
        return None    
#返回大图页上图片的链接和标题
def parse_page_detail(html):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()

def main():
    html = get_page_index(0,'街拍')
    # for item in parse_page_index(html):
    #     print(item)
    detail_html = get_page_detail('http://toutiao.com/group/6335650371411902721/')   
    print(detail_html)
if __name__=='__main__':
    main()
