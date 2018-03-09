import requests
import json
from urllib.parse import urlencode
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
from hashlib import md5
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
    driver = webdriver.Firefox()
    driver.get(url)
    WebDriverWait(driver,2)    
    source =  driver.page_source
    driver.quit()
    return source

  
#返回大图页上图片的链接和标题
def parse_page_detail(html):
    soup = BeautifulSoup(html,'lxml')
    src_list=[]
    title=''
    try:
        for item in soup.find('div',class_='article-content'):
            for pic in item.find_all('img'):
                src_list.append(pic.get('src'))
        title = soup.select('title')[0].get_text()
    except:
        pass
    return title,src_list

def pic_download(title,pic_url,img_src):
    if pic_url:
        current_path = os.getcwd()
        path = current_path+'/{}'.format(img_src[-8:-1])
        if not os.path.exists(path):
            os.makedirs(path)
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
                print('图片下载出错',image)
def main():
    html = get_page_index(0,'街拍')
    for item in parse_page_index(html): 
        if item:
            detail_html = get_page_detail(item)   
            title,pic_src = parse_page_detail(detail_html)
            pic_download(title,pic_src,item)
        else:
            pass
if __name__=='__main__':
    main()
