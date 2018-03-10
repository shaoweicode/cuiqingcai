import requests
import json
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
from hashlib import md5


def login(Browser):
    # 登录新浪微博，返回带cookie的浏览器句柄
    login_url = 'https://passport.weibo.cn/signin/login'
    Browser.get(login_url)
    input_box_name = WebDriverWait(Browser,10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'#loginName'))
    )
    ActionChains(Browser).click(input_box_name).perform()
    input_box_name.send_keys('13940220362')
    input_box_password =WebDriverWait(Browser,5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'#loginPassword'))
    )
    input_box_password.send_keys('13355652156')
    WebDriverWait(Browser,5)
    Button = Browser.find_element_by_css_selector('#loginAction')
    Button.click()
    return Browser
if __name__=='__main__':
    driver = webdriver.Firefox()
    driver = login(driver)
    yuelao = 'https://m.weibo.cn/u/5579100681'
    driver.get(yuelao)
    