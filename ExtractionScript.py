
# coding: utf-8

# In[1]:

import pandas as pd
import re 
import sys

df = pd.read_csv(sys.argv[1])


# In[2]:

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


# In[ ]:




# In[3]:

if (sys.argv[2] == True):
    f = open('youtubeComments.xml', 'w')
    f.write('<dialogue> \n')
    f.close()


# In[4]:

df['commentText'].str.replace(r"IsHan","")
df


# In[5]:

import re
for n in re.findall(r'[^\u4e00-\u9fff，。／【】、；‘:""]+',df.iloc[2].commentText):
    print (n)


# In[6]:

df['commentText'] = df['commentText'].str.replace(r"[^\u4e00-\u9fff，。／【】、；‘:""\d]+","")
df['repliesCommentText'] = df['repliesCommentText'].str.replace(r"[^\u4e00-\u9fff，。／【】、；‘:""\d]+","")



# In[7]:

df = df[df.commentText != '']
df = df[df.repliesCommentText != '']
df = df.reset_index()
df


# In[17]:

users = []

f = open('youtubeComments.xml', 'a')
for i in range(0, df.index.size-1):
    if (pd.isnull(df.iloc[i].user) == False) and (pd.isnull(df.iloc[i+1].user) == False): #deals with case where there are no replies
        uttid = 1
        s = '\t<s> \n'.expandtabs(4)
        s += '\t< utt uid=\"'.expandtabs(8)
        s += str(uttid)
        s += '\">'
        s += str(df.iloc[i].commentText)
        s += '</utt>\n'
        s+= '\t</s> \n'.expandtabs(4)
        f.write(s)
    elif (pd.isnull(df.iloc[i+1].user) == True) and (pd.isnull(df.iloc[i].user) == False):
        users = []
        users.append(df.iloc[i].user)
        uttid = 1
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
            if not (pd.isnull(df.iloc[j].user)):
                if df.iloc[j].user in users: #name already exists
                    a = a+1
                else:
                    users.append(df.iloc[j].user)
            else:
                if df.iloc[j].repliesUser in users:
                    a = a+1
                else:
                    users.append(df.iloc[j].repliesUser)
            uttid = users.index(df.iloc[j].repliesUser) + 1
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


# In[10]:

users


# In[ ]:

df


# In[ ]:

if (sys.argv[3] == True):
    f = open('youtubeComments.xml', 'a')
    f.write('</dialogue>')


# In[ ]:



