# -*- coding: utf-8 -*-
import scrapy
import json
from selenium import webdriver
import time
import pickle

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu2'
    #allowed_domains = ['https://www.zhihu.com/']
    start_urls = ['https://www.zhihu.com/']
    loginUrl = 'https://www.zhihu.com/#signin'
    siginUrl = 'https://www.zhihu.com/login/email'

    feedUrl = 'https://www.zhihu.com/api/v3/feed/topstory'
    nextFeedUrl = ''
    curFeedId = 0

    custom_settings = {
        "COOKIES_ENABLED": True,
        "ROBOTSTXT_OBEY": False,
    }

    headers = {
        'Host':
        'www.zhihu.com',
        'Connection':
        'keep-alive',
        'Origin':#not found
        'https://www.zhihu.com',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
        'Content-Type':
        'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'X-Requested-With': #not found
        'XMLHttpRequest',
        'Referer':#not found
        'https://www.zhihu.com/',
        'Accept-Encoding':
        'gzip, deflate, br',
        'Accept-Language':
        'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
        'Upgrade-Insecure-Requests:':
        1,
        'Cache-Control':
        'no-cache',

    }

    cookies = {
        'q_c1':
        '104b8db5939b4a819631957e62288879|1505702657000|1505702657000',
        'q_c1':
        '647915bd7d304d78b0641dc937fe8bff|1505702657000|1505702657000',
        '_zap':
        '73489605-e464-4d77-8bf5-21cb2a73876a',
        'r_cap_id':
        '"YTZhNjgzNDIxY2QxNDVmMjg1MTMyMTQ2YWJjZTUyODc=|1505702660|b6cbbe4770565f83e297187213624abf7d229176"',
        'cap_id':
        '"NDUzNTU0Yzc5M2Q5NGEyNTliODNjYmE1YmZmZTc1NzQ=|1505702660|b55d910ca1f34d4ce74426c03de26a11707ccb74"',
        'd_c0':
        '"ABDC2n3LZAyPTmKmcSfpxfYSYP573DCXETs=|1505702660"',
        's-q':
        '%E7%9F%A5%E4%B9%8E%20%E7%88%AC%E8%99%AB',
        's-i':
        '6',
        'sid':
        'ec9o9vjg',
        'z_c0':
        'Mi4xZGF0U0FBQUFBQUFBRU1MYWZjdGtEQmNBQUFCaEFsVk5Dc0xtV1FEZV8zN1gxa0E2Tkk3TmF6WVBRbF9mMU5RNUZ3|1505703178|8769d9497e50ae42a66c8b06274f02f36c9a59b1',
        'l_n_c':
        '1',
        '__utma':
        '51854390.1609852963.1505702661.1505702661.1505702661.1',
        '__utmb':
        '51854390.0.10.1505702661',
        '__utmc':
        '51854390',
        '__utmv':
        '51854390.000--|3=entry_date=20170917=1',
        '__utmz':
        '51854390.1505702661.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/29925879',
        '_xsrf':
        '067f7563-5fbd-47dc-902b-0b7b40aa18bc',


    }
    def parse(self, response):
        thefile = open('body.txt', 'w')
        thefile.write(response)
        print('...........................')
        print(response)
        thefile.close()
  #      self.driver = webdriver.Chrome('C:/chromedriver.exe')
   #     self.driver.get(response.url)
   #     self.driver.save_screenshot('screenie.png')

    def start_requests(self):
        return [
            scrapy.http.FormRequest(
                self.loginUrl,
                headers=self.headers,
                cookies=self.cookies,
                meta={'cookiejar': 1},
                callback=self.post_login)
        ]

    def post_login(self, response):
        xsrf = response.css(
            'div.view-signin > form > input[name=_xsrf]::attr(value)'
        ).extract_first()
        self.headers['X-Xsrftoken'] = xsrf

        return [
            scrapy.http.FormRequest(
                self.siginUrl,
                method='POST',
                headers=self.headers,
                meta={'cookiejar': response.meta['cookiejar']},
                formdata={
                    '_xsrf': xsrf,
                    'captcha_type': 'cn',
                    'email': 'xxxxxx@163.com',
                    'password': 'xxxxxx',
                },
                callback=self.after_login)
        ]

    def after_login(self, response):
        jdict = json.loads(response.body)
        print('after_login', jdict)
        if jdict['r'] == 0:
            z_c0 = response.headers.getlist('Set-Cookie')[2].split(';')[
                0].split('=')[1]
            self.headers['authorization'] = 'Bearer ' + z_c0
            return scrapy.http.FormRequest(
                url=self.feedUrl,
                method='GET',
                meta={'cookiejar': response.meta['cookiejar']},
                headers=self.headers,
                formdata={
                    'action_feed': 'True',
                    'limit': '10',
                    'action': 'down',
                    'after_id': str(self.curFeedId),
                    'desktop': 'true'
                },
                callback=self.parse)
        else:
            print(jdict['error'])




    def next_request(self, response):
        return scrapy.http.FormRequest(
            url=self.nextFeedUrl,
            method='GET',
            meta={'cookiejar': response.meta['cookiejar']},
            headers=self.headers,
            callback=self.parse)

