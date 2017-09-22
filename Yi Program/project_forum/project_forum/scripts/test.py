# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pickle
import scrapy
import json
import time
import re
import os
import requests
from selenium import webdriver
from lxml import html
class conversation_builder():
    conversation_id = 0
    user_id = 0
    total_conversations = 0
    # container for Starter
    starter = []
    # container for follower
    follower = []
    total_follower = []
    # container for texts
    conversations = []
    def add(self,comment):
        if comment.find_all("span", "desc"):
            self.new_thread(comment)
        else:
            self.new_reply(comment)
    def new_thread(self,comment):
        self.total_conversations += 1
        self.starter.append(comment.find("a", "zg-link author-link").get("title"))
        print(self.starter[self.total_conversations - 1])
    def new_reply(self,comment):
        pass


cb = conversation_builder()

user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
headers = {'User-Agent': user_agent,
           'Upgrade-Insecure-Requests': '1',
           'Cache-Control': 'max-age=0',
           'keep-alive': 'timeout=40, max=300',
           }
url = "https://www.zhihu.com/node/AnswerCommentListV2?params=%7B%22answer_id%22%3A%"+"2215184366"+"%22%7D"



r = requests.get(url, headers=headers, allow_redirects = True)
soup = BeautifulSoup(r.text,"lxml")
soup.prettify()
for comment in soup.find_all("div", "zm-item-comment"):
    try:
        p = comment.find("div", "zm-comment-hd").text
    #cb.add(comment)
    except: pass

url = "https://www.zhihu.com/node/AnswerCommentListV2?params=%7B%22answer_id%22%3A%"+"2215184366"+"%22%7D"
res = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
soup = BeautifulSoup(res.text,"lxml")
for item in soup.select(".zm-item-comment"):
    author2 = "abc"
    try:
        author2 = item.select(".author_link")[1].text
    except: pass
    try:
        author = item.select(".author-link")[0].text

        comment = item.select(".zm-comment-content")[0].text
       # print(author,comment)
        print(author, author2, comment)
    except:pass