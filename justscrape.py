import csv
import itertools
import codecs
import re
import os
import requests
from random import randint
from pandas import DataFrame
from pandas import ExcelWriter
headers = {
	'Connection': 'keep-alive',
	'Pragma': 'no-cache',
	'Cache-Control': 'no-cache',
	'Upgrade-Insecure-Requests': '1',
	'DNT': '1',
	'Content-Type': 'application/x-www-form-urlencoded',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'en-US,en;q=0.9',
	}
def getProxy():
	try:
		proxies = {}
		url = "https://www.proxynova.com/proxy-server-list/country-in/"
		proxypage = requests.get(url,headers=headers)
		proxypage = proxypage.text
		proxyip = re.findall(r'<abbr title="(.*?)"><script>',proxypage,re.DOTALL)[0]
		proxyport = re.findall(r'<a href="/proxy-server-list/port-(.*?)/" title=',proxypage,re.DOTALL)[0]
		proxy = str(proxyip)+':'+str(proxyport)
		proxies['http'] = proxy
		proxies['https'] = proxy
	except:
		proxies = "Not found"
	return proxies
def getName(body):
	try:
		name = re.findall(r'Ratings for (.*?)class="rating_div" >',body,re.DOTALL)[0]
		name = str(name)
		name = name.split(" in ",1)[0]
		name = str(name)
	except:
		name = "Not found"
	return name
def getPhone(body):
	try:
		phone = re.findall(r'<i class="res_contactic resultimg"></i><span><a>(.*?)</a></span>',body,re.DOTALL)[0]
		phone = str(phone)
		phone = phone.replace('<span class="',"")
		phone = phone.replace('"></span><span class="',"")
		phone = phone.replace('"></span>',"")
		phone = phone.replace("mobilesv icon-dc","")
		phone = phone.replace("mobilesv icon-fe","")
		phone = phone.replace("mobilesv icon-hg","")
		phone = phone.replace("mobilesv icon-ba","")
		phone = phone.replace("mobilesv icon-ji","9")
		phone = phone.replace("mobilesv icon-yz","1")
		phone = phone.replace("mobilesv icon-rq","5")
		phone = phone.replace("mobilesv icon-wx","2")
		phone = phone.replace("mobilesv icon-lk","8")
		phone = phone.replace("mobilesv icon-acb","0")
		phone = phone.replace("mobilesv icon-ts","4")
		phone = phone.replace("mobilesv icon-nm","7")
		phone = phone.replace("mobilesv icon-vu","3")
		phone = phone.replace("mobilesv icon-po","6")
		phone = phone[2:]
	except:
		phone = "Not found"
	return phone
def getRating(body):
	try:
		rating = re.findall(r'<span class="exrt_count">(.*?)</span>',body,re.DOTALL)[0]
		rating = str(rating)
	except:
		rating = "Not Found"
	return rating
def getAddress(body):
	try:
		address = re.findall(r'<span class="cont_fl_addr">(.*?)</span>',body,re.DOTALL)[0]
		address = str(address)
	except:
		address = "Not found"
	return address
def getLocation(body):
	try:
		location = re.findall(r'Ratings for (.*?)class="rating_div" >',body,re.DOTALL)[0]
		location = location.split(" in ",1)[-1]
		location = location.split(",",1)[0]
		location = str(location)
	except:
		location = "Not found"
	return location
def getCity(body):
	try:
		city = re.findall(r'Ratings for (.*?)class="rating_div" >',body,re.DOTALL)[0]
		city = city.split(" in ",1)[-1]
		city = city.split(",",1)[-1]
		city = city[1:]
		city = city.replace("\\","")
		city = city.replace("' ","")
		city = str(city)
	except:
		city = "Not found"
	return city
def getImage(body):
	try:
		image = re.findall(r'data-src="(.*?)fit=around',body,re.DOTALL)[0]
		image = str(image)
		image = image[:-1]
	except:
		image = "None"
	return image
def getSession():
	# proxies = getProxy()
	s = requests.Session()
	# s.proxies = proxies
	return s
def scrape(URL,pages):
	pageNumber = 1
	pages = int(pages)
	data = []
	while pageNumber <= pages:
		try:
			URL = URL.replace("https://t.","https://www.")
		except:
			pass
		link = URL+"/page-%s" % (pageNumber)
		s = getSession()
		try:
			page = s.get(link,headers=headers)
		except:
			s = getSession()
			page = s.get(link,headers=headers)
		page = page.text
		a = re.findall(r'<!-- #Cards start here -->(.*?)<!--- #Cards Ends Here -->',page,re.DOTALL)
		for i in a:
			listingDict = {}
			Name = getName(i)
			Phone = getPhone(i)
			Rating = getRating(i)
			Address = getAddress(i)
			Location = getLocation(i)
			City = getCity(i)
			Image = getImage(i)
			listingDict['Name'] = Name
			listingDict['Phone'] = Phone
			listingDict['Rating'] = Rating
			listingDict['Address'] = Address
			listingDict['Location'] = Location
			listingDict['City'] = City
			listingDict['Image'] = Image
			data.append(listingDict)
		pageNumber += 1
	header = data[0].keys()
	t = DataFrame(data)
	filename = "js"+str(randint(0,2324))+".csv"
	# writer = ExcelWriter(filename, engine='xlsxwriter')
	# t.to_excel(writer,'Sheet2', encoding='utf-8', index=False, columns=header)
	# writer.save()
	t.to_csv(filename,index=False)
	return filename