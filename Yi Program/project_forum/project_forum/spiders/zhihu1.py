# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
import scrapy
import json
import time
import re
import os


# 知乎问答爬虫
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu1'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # 伪造请求头
    headers = {
        'Connection': 'Keep-Alive',
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
    }
    # 知乎首页
    index_url = "https://www.zhihu.com/"
    # 验证码
    _captcha = ""
    # 请求令牌，防止跨站伪造请求
    _xsrf = ""

    # 如果callback不指定，默认调用parse方法
    def parse(self, response):
        self.driver = webdriver.Chrome('C:/Users/Yi/PycharmProjects/COMP551A1/Yi Program/project_forum/project_forum/spiders/chromedriver.exe')
        self.driver.get('https://www.zhihu.com/explore#daily-hot')
        time.sleep(2)
        #a = self.driver.find_element_by_css_selector('div.zm-item-answer>link').get_attribute('href')
        #a = [i.get_attribute('href') for i in self.driver.find_elements_by_css_selector('div.zm-item-answer>link')]
        a = self.driver.find_element_by_css_selector('div.zm-meta-panel>a.meta-item.toggle-comment.js-toggleCommentBox').click()

        print(".....................................")
        print(a)
        print(".....................................")

        self.driver.save_screenshot('screenie.png')
        self.driver.close()
        yield {
            "url": response.url,

        }

    # 爬取内容
    def parse_detail(self, response):
        pass

    # 知乎需要登录，重写start_request入口方法，首先请求验证码->人工识别输入验证码->登录->爬取
    def start_requests(self):

        random = time.time() * 1000
        # 小技巧：type=en是英文验证码，英文验证码比中文容易
        captcha_url = "https://www.zhihu.com/captcha.gif?&type=login&lang=en&r=" + str(random)
        return [
            scrapy.Request(
                url=captcha_url,
                headers=self.headers,
                callback=self.download_captcha
            )
        ]

    # 下载验证码
    def download_captcha(self, response):
        path = os.path.abspath(os.path.dirname(__file__))
        with open(path + "/captcha.gif", "wb") as f:
            f.write(response.body)
            f.close()
        self._captcha = input("输入验证码: ")
        return [
            scrapy.Request(
                url=self.index_url,
                headers=self.headers,
                callback=self.login
            )
        ]

    # 登录，只做了邮箱登录一样
    def login(self, response):
        # 获取请求令牌
        xsrfs = response.xpath("//input[@name='_xsrf']").extract()
        if xsrfs is not None:
            self._xsrf = re.compile(r'[\s\S]*type="hidden" name="_xsrf" value="(.*?)".*').match(xsrfs[0]).group(1)

        # 使用手机登录
        params = {
            "phone_num": "5146622955",
            "password": "sy1995422",
            "_xsrf": self._xsrf,
            "captcha": self._captcha
        }

        return [
            scrapy.FormRequest(
                url="https://www.zhihu.com/login/phone_num",
                headers=self.headers,
                callback=self.check_login,
                formdata=params
            )
        ]

    def check_login(self, response):
        rel = json.loads(response.text)
        if rel is not None and rel['r'] == 0:
            # 如果登录成功回到首页继续爬取
            for url in self.start_urls:
                yield scrapy.Request(url=url, headers=self.headers, dont_filter=True)
        else:
            print("登录失败")