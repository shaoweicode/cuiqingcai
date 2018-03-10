import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
#设置cookie，headers
cookie = {'Cookie':'_T_WM=8a8a80bbf475978669146aae50b11636; SUB=_2A253p_7IDeRhGeVP6VsQ8yvPwzuIHXVVa4KArDV6PUJbkdANLVLdkW1NTUOLwB6VzDsaSro94umj0qvjPeNwS15l; SUHB=09PNEom02nY695; SCF=AgGcWqM_07cf5R9Gv2fdSl-AuYhehBds8YT2N-mpORrWh8yFK5nE5NYsLgJp7Wn68mX2LbE2CqwTDnPRpSz2XDw.; SSOLoginState=1520668337; M_WEIBOCN_PARAMS=featurecode%3D20000320%26oid%3D4048737515517195%26luicode%3D10000011%26lfid%3D1076035579100681%26uicode%3D20000174%26fid%3Dhotword'}
headers = {'User-Agent':'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1C28 Safari/419.3'}
#api接口请求，返回的是json格式的数据
def get_index_page(page,current_cookie,headers):
    url_template = 'https://m.weibo.cn/api/container/getIndex?'
    data = {
    'type':'uid',
    'value':5579100681,
    'containerid':'1076035579100681',
    'page':page
    }
    url = url_template+urlencode(data)
    try:
        response = requests.get(url,cookies = current_cookie,headers = headers)
    except:
        return None
    return response.text
#解析json 返回当前页上，每条微博的地址
def parse_page_index(jsondata):
    if jsondata:
        weibo_list = []
        data_dict = json.loads(jsondata)
        for item in data_dict['data']['cards']:
            if 'scheme' in item.keys():
                weibo_list.append(item['scheme'])
        return weibo_list
    else:
        return None
# def browser_open():
#     driver = webdriver.Firefox()
#     return driver

def get_detail_page(url_list,Browser):
    if url_list:
        html = []
        for weibo in url_list:
            Browser.get(weibo)
            WebDriverWait(Browser,3)
            html.append(Browser.page_source)
        return html
    else:
        return None

def main():
    driver = webdriver.Firefox()
    json_data = get_index_page(2,cookie,headers)
    weibo_detail_list = parse_page_index(json_data)
    get_detail_page(weibo_detail_list,driver)

if __name__=='__main__':
    main()