# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pickle
import requests
class conversation_builder():

    user_id = 0  #index holder
    total_conversations = 0
    # container for Starter of one conversation
    starter = []
    # container for follower of each conversation
    follower = []
    # track the total number of follower, if new follower come, easy to identify the uid
    # excluding starter
    total_follower = []
    # container for texts
    conversations = []
    def add(self,comment):
        try: #is it a reply ?
            listener = comment.select(".author-link")[1].text #if keyword "回复" is not found, then it is not a reply, the next line of code won't be executed
            self.new_reply(comment,listener)
        except:
            self.new_thread(comment)
    def new_thread(self,comment):
        author = comment.select(".author-link")[0].text
        text = comment.select(".zm-comment-content")[0].text.strip()
        # Does the author started a converstaion already?
        if any(author in people for people in self.starter):
            return 0
        else:
            self.total_conversations += 1
            formatted_text = "<s><utt uid=\"1\">" + text + "</utt>"
            self.starter.append(author)
            self.conversations.append(formatted_text)
            self.total_follower.append(0)
    def new_reply(self,comment,listener):
        text = item.select(".zm-comment-content")[0].text.strip()
        author = item.select(".author-link")[0].text
        # does the author started this conversation ? (owner of this conversation?)
        if any(author in people for people in self.starter):
            uid = 1
            conversation_id = self.starter.index(author)
        # does the author is an exsisting follower?
        if any(author in followers for followers in self.follower):
            follower_list = [followers for index, followers in enumerate(self.follower) if author in followers]
            conversation_id = [index for index, followers in enumerate(self.follower) if author in followers]
            followers = str(follower_list).strip('[]').split()
            uid = followers.index(author) + 2 # +1 compensate for 0, +1 compensate for starter, totally +2
        else: #this means that the author is a new follower
            # is this author replying to a starter?
            if not any(listener in people for people in self.starter): #Find the place of this conversation by listener
                conversation_id = [index for index, followers in enumerate(self.follower) if listener in followers]
            else: # this means the author is a new follower and is replying to the starter
                conversation_id = self.starter.index(listener)
            if self.total_follower == 0:
                self.follower[conversation_id] += " " + author
            else:
                self.follower.append(" " + author)
            self.total_follower[conversation_id] += 1
            uid = self.total_follower[conversation_id] + 2  # +1 compensate for new follower, +1 compensate for starter, totally +2
            # check if this new follower is the first new follower

        self.conversations[conversation_id] += "<s><utt uid=\"%s\">" %uid + text + "</utt>"








user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
headers = {'User-Agent': user_agent,
           }


url = "https://www.zhihu.com/node/AnswerCommentListV2?params=%7B%22answer_id%22%3A%"+"2215184366"+"%22%7D"
cb = conversation_builder()
r = requests.get(url, headers=headers, allow_redirects = True)
soup = BeautifulSoup(r.text,"lxml")
soup.prettify()
for item in soup.select(".zm-item-comment"):
    try:
        author = item.select(".author-link")[0].text
        cb.add(item)
    except: pass

db = open('db.txt', 'wt', encoding='utf-8')
for item in cb.conversations:
    db.write("%s</s>\n" % item)
db.close()

