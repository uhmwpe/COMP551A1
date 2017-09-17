
# coding: utf-8

# In[8]:

import pandas as pd
import pickle
import re
import sys

with open("test.txt", "rb") as fp:
    b = pickle.load(fp)
users = b
df = pd.read_csv(sys.argv[1])


# In[9]:

##Data Cleaning cecll

df.iloc[2].user
df.drop('replies.id', axis=1, inplace=True)
df.drop('replies.date', axis=1, inplace=True)
df.drop('replies.timestamp', axis=1, inplace=True)
df.drop('replies.likes', axis=1, inplace=True)
df.drop('id', axis=1, inplace=True)
df.drop('timestamp', axis=1, inplace=True)
df.drop('likes', axis=1, inplace=True)
df.drop('date', axis=1, inplace=True)

df.rename(columns={'replies.commentText': 'repliesCommentText', 'replies.user': 'repliesUser'}, inplace=True)


# In[10]:

##Chinese comments only

df['commentText'] = df['commentText'].str.replace(r"[^\u4e00-\u9fff，。／【】、；‘:""]+","")
df['repliesCommentText'] = df['repliesCommentText'].str.replace(r"[^\u4e00-\u9fff，。／【】、；‘:""]+","")
df = df[df.commentText != '']
df = df[df.repliesCommentText != '']
df = df.reset_index()


# In[12]:

##appending to users
for i in range(0, df.index.size): #pd.isnull checks for nan
    if not (pd.isnull(df.iloc[i].user)):
        if df.iloc[i].user in users: #name already exists
            continue
        else:
            users.append(df.iloc[i].user)
    else:
        if df.iloc[i].repliesUser in users:
            continue
        else:
            users.append(df.iloc[i].repliesUser)



# In[13]:

### Appending into youtubeComments.xml
f = open('youtubeComments.xml', 'a')
for i in range(0, df.index.size-1):
    if (pd.isnull(df.iloc[i].user) == False) and (pd.isnull(df.iloc[i+1].user) == False): #deals with case where there are no replies
        uttid = users.index(df.iloc[i].user)
        s = '\t<s> \n'.expandtabs(4)
        s += '\t< utt uid=\"'.expandtabs(8)
        s += str(uttid)
        s += '\">'
        s += str(df.iloc[i].commentText)
        s += '</utt>\n'
        s+= '\t</s> \n'.expandtabs(4)
        f.write(s)
    elif (pd.isnull(df.iloc[i+1].user) == True) and (pd.isnull(df.iloc[i].user) == False):
        uttid = users.index(df.iloc[i].user)
        s = '\t<s> \n'.expandtabs(4)
        s += '\t< utt uid=\"'.expandtabs(8)
        s += str(uttid)
        s += '\">'
        s += str(df.iloc[i].commentText)
        s += '</utt>\n'
        if (i<df.index.size - 1):
            j = i+1
            
        a = 0
        
        while((pd.isnull(df.iloc[j].user)==True) and (j<(df.index.size - 1))):
            uttid = users.index(df.iloc[j].repliesUser)
            s += '\t< utt uid=\"'.expandtabs(8)
            s += str(uttid)
            s += '\">'
            s += df.iloc[j].repliesCommentText
            s += '</utt>\n'
            j += 1
           
        i = j
        s+= '\t</s> \n'.expandtabs(4)
        f.write(s)
            
        

f.close()


# In[ ]:

###writing list 
with open("test.txt", "wb") as fp:
    pickle.dump(users, fp)

