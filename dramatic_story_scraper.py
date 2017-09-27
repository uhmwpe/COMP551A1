import requests
import string
from bs4 import BeautifulSoup
from lxml import etree

#starting text
starttext = '场 景：'

#character information
charinfo = '人 物：'

char_dict = {'石铁牛：':1,'李萍：':2}
char_list = ['石铁牛：','李萍：']
#halting point
endtext = '大 纲： '

#drama script, scraper
url = "http://www.juben108.com/hjxs_82328_1/"
r = requests.get(url)

soup = BeautifulSoup(r.content)

links = soup.find_all("table", {"class": "neiyehg"})
textdiv = links[0].find_all("div")
f = lambda x: str.replace(x.text, '\xa0', '')
intermediatelist = list(filter(None, [f(x) for x in textdiv]))

#extra information indexing
endpoint = intermediatelist.index(endtext)

newtextlist = intermediatelist[:(endpoint -1)]

startindices = [i for i, s in enumerate(newtextlist) if starttext in s]

headerlesslist = newtextlist[(startindices[0]+1):]

finallist = [x for x in headerlesslist if char_list[0] in x or char_list[1] in x]

def xmlcreator(finallist):
	page = etree.Element('dialog')
	doc = etree.ElementTree(page)
	conv = etree.SubElement(page, 's')
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
				utt.text = line
	etree.dump(page)


