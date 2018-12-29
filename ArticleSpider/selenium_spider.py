# -*- coding: utf-8 -*-

from selenium import webdriver
from scrapy.selector import Selector

browser = webdriver.Chrome(executable_path="/Users/liutanqi/scrapy_project/ArticleSpider/ArticleSpider/chromedriver")
browser.get("https://www.zhihu.com/signup?next=%2F")

browser.find_element_by_xpath('//div[@class="SignContainer-switch"]/span').click()
browser.find_element_by_xpath('//div[@class="SignFlow-accountInput Input-wrapper"]/input').send_keys('18524060284')
browser.find_element_by_xpath(
    '//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[2]/div/div[1]/input').send_keys('hanbaobao0315')
browser.find_element_by_xpath('//button[@class="Button SignFlow-submitButton Button--primary Button--blue"]').click()

import time

time.sleep(10)

browser.execute_script(
    "window.scrollTo(0,document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage")
# for i in range(3):
#     browser.execute_script(
#         "window.scrollTo(0,document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage")
#     time.sleep(3)
# browser.quit()


###############################

# 淘宝镜像

# http://npm.taobao.org/mirrors
# http://selenium-python.readthedocs.io/installation.html


###############################
