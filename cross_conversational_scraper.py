import requests
import re
import string
from bs4 import BeautifulSoup
from lxml import etree

#soup array
souplistFirst =["http://www.juben108.com/xiangsheng_54033_1/",
			    "http://www.juben108.com/xiangsheng_77714_1/"]
souplistSecond = ["http://www.juben108.com/xiangsheng/Show.asp?ID=75941"]
souplistP = ["http://www.juben108.com/xiangsheng/Show.asp?ID=49971",
			 "http://www.juben108.com/xiangsheng_77995_1/", #tagged as bad
			 "http://www.juben108.com/xiangsheng/Show.asp?ID=53368"]

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

def pseudoFirst():
	char_list = ['乙：','甲：']

	#dataCleaner(souplistFirst, char_list, "div")
	dataCleaner(souplistP, char_list, "p")

def pseudoSecond():
	char_list =['商宝：','叶贝：']

	dataCleaner(souplistSecond, char_list, "div")

def dataCleaner(souplist, char_list, internaltag):
	for url in souplist:
		char_dict = {}
		r = requests.get(url)

		soup = BeautifulSoup(r.content, "lxml")

		links = soup.find_all("table", {"class": "neiyehg"})
		textdiv = links[0].find_all(internaltag)
		f = lambda x: str.replace(x.text, '\xa0', '')
		intermediatelist = list(filter(None, [f(x) for x in textdiv]))
		finallist = makeFinalList(intermediatelist, char_list, char_dict)
		xmlCreator(finallist, char_list, char_dict)

def makeFinalList(list, char_list, char_dict):
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


pseudoFirst()
#pseudoSecond()
#pseudoThird()
etree.dump(dialog)