import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re
import os
from hashlib import md5
import time
#设置cookie，headers
cookie = {'Cookie':'_T_WM=7575d015224732055b001c4424bc997c; SUB=_2A253oWKSDeRhGeVP6VsQ8yvPwzuIHXVVag7arDV6PUJbkdBeLUT9kW1NTUOLwA0pqT8x6a7A5v2jolQqmWFJdf4D; SUHB=09PNEom02nZFDX; SCF=Al6znnPnj-aWNZi2az-UyUP6UjKZwjycPB7ChQSpF7n950moFnA50nq9_xlTvO6jpacyUSxaoglZVmTIB5cRemQ.; M_WEIBOCN_PARAMS=featurecode%3D20000320%26oid%3D4216162608477453%26lfid%3Dhotword%26luicode%3D20000173%26uicode%3D20000174%26fid%3Dhotword'}
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
#返回URL-list中每条微博的网页源代码
def get_detail_page(url_list,headers):
    if url_list:
        html = []
        for weibo in url_list:
            response = requests.get(weibo,headers = headers)
            html.append(response.text)
        return html
    else:
        return None
#解析html，返回每条微博的标题和图片地址
def parse_detail_page(html): 
    pattern = re.compile(r'#\D\D\D\D#\D*<a')
    text = pattern.findall(html)
    
    if text:
        if '女嘉宾' in text[0]:       
            pic_src=[]
            pattern = re.compile(r'"url":.*jpg')
            all_pic = pattern.findall(html)
            pattern_title = re.compile(r'@\S*</a>')
            title = pattern_title.findall(html)[0]
            for item in all_pic:
                if 'large' in item:
                    pic_src.append(item.strip('"url": '))            
            return title,pic_src
        else :
            return None,None
    else:
        return None,None
    
    
def pic_download(title,pic_url):
    # path = '/home/shaowei/cuiqingcai/img'
    if pic_url:
        path = '/home/shaowei/cuiqingcai/{}'.format(title[1:-4])
        if not os.path.exists(path):
            os.mkdir(path)
        for image in pic_url:
            response = requests.get(image)
            if response.status_code==200:
                content = response.content
                file_path = path+'/'+'{}'.format(md5(content).hexdigest())+'.jpg'
                if not os.path.exists(file_path):
                    with open(file_path,'wb') as f:
                        f.write(content)
                        f.close()
                        print(file_path,'下载完成')
            else:
                pass
    else:
        pass

def main():
    for page_num in range(3,10):
        try:
            time.sleep(5)
            json_data = get_index_page(page_num,cookie,headers)
            weibo_detail_list = parse_page_index(json_data)
            html = get_detail_page(weibo_detail_list,headers)
            for item in html:
                time.sleep(3)
                try:
                    title,pic_add = parse_detail_page(item)        
                    pic_download(title,pic_add)
                except:
                    pass
        except:
            pass
        # print(pic_add)
    
    
    

if __name__=='__main__':
    main()