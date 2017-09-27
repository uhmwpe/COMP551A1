import requests
import re
import string
from bs4 import BeautifulSoup
from lxml import etree
souplist = ["http://www.juben68.com/apple/3269.html"]
# #soup array
# souplistFirst =["http://www.juben108.com/xiangsheng_54033_1/",
# 			    "http://www.juben108.com/xiangsheng_77714_1/"]
# souplistSecond = ["http://www.juben108.com/xiangsheng/Show.asp?ID=75941"]
# souplistP = ["http://www.juben108.com/xiangsheng/Show.asp?ID=49971",
# 			 "http://www.juben108.com/xiangsheng_77995_1/", #tagged as bad
# 			 "http://www.juben108.com/xiangsheng/Show.asp?ID=53368"]

def printlist(list):
	for item in list:
		print(item)

#halting point

#drama script, scraper
# url = "http://www.juben108.com/xiangsheng_54033_1/"
# r = requests.get(url)

# soup = BeautifulSoup(r.content)

# links = soup.find_all("table", {"class": "neiyehg"})
# textdiv = links[0].find_all("div")
# f = lambda x: str.replace(x.text, '\xa0', '')
# intermediatelist = list(filter(None, [f(x) for x in textdiv]))

dialog = etree.Element('dialog')
doc = etree.ElementTree(dialog)
locationtag = '地点：'

# def pseudoFirst():
# 	char_list = ['乙：','甲：']

# 	#dataCleaner(souplistFirst, char_list, "div")
# 	dataCleaner(souplistP, char_list, "p")

# def pseudoSecond():
# 	char_list =['商宝：','叶贝：']

# 	dataCleaner(souplistSecond, char_list, "div")

def getSplitLists(list):
	returnlist = []
	x =0
	for i, item in enumerate(list):
		if re.search("第[一二三四五六七八九]幕", item):
			newlist = list[x:i]
			if len(newlist) == 0:
				break
			if len(newlist[0]) != 0:
				returnlist.append(newlist)
			x = i+1
	returnlist.append(list[x:])
	return returnlist[1:]

def makeColonLists(list):
	oglist = []
	for item in list:
		newlist = []
		for y in item:
			if '：' in y:
				newlist.append(y)
		oglist.append(newlist)
	return oglist

def fillCharacterList(list):
	nameset = set()
	for item in list:
		name, text = item.split('：')
		nameset.add(name)
	return nameset
#http://www.juben68.com/apple/3240.html
#"http://www.juben68.com/apple/3269.html"
def dataCleaner(souplist=["http://www.juben68.com/apple/3240.html"]):
	for url in souplist:
		char_dict = {}
		r = requests.get(url)
		soup = BeautifulSoup(r.content, "lxml")
		links = soup.find_all("div", {"id": "paragraph"})
		headerless = links[0].find("p").extract()
		textdiv = links[0].find_all("p")
		f = lambda x: re.sub("([\n\r\t])|http://www.juben68.com", "", x.text)
		intermediatelist = list(filter(None, [f(x) for x in textdiv]))
		introless = list(filter(lambda x: x.find('地点：') == -1, intermediatelist))
		#get indices
		splitlists = getSplitLists(introless)
		colonlists = makeColonLists(splitlists)
		#further filter with colons
		for llist in colonlists:
			char_set = fillCharacterList(llist)
			#make final list
			xmlCreator(llist, char_set, char_dict)
			#finallist = makeFinalList(intermediatelist, char_set, char_dict)
		#xmlCreator(finallist, char_list, char_dict)

def makeFinalList(list, char_set, char_dict):
	newtextlist = []
	for line in list:
		for char in char_list:
			if char in line:
				newtextlist.append(line)
	return newtextlist

def xmlCreator(finallist, char_list, char_dict):
	conv = etree.SubElement(dialog, 's')
	i = 0
	for line in finallist:
		for char in char_list: 
			if char in line:
				if char not in char_dict:
					i = i+1
			
					char_dict[char] = i
				#if char already exists then don't add
				utt = etree.SubElement(conv, 'utt')
				utt.attrib["uid"] = str(char_dict[char])
				utt.text = line.replace(char, "")


dataCleaner()
#pseudoSecond()
#pseudoThird()
etree.dump(dialog)