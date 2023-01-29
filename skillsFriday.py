from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from googlesearch import search
from datetime import datetime
import requests
import wikipedia
import yfinance as yf


def openWebsite(websiteName):
	chrome_options = Options()
	chrome_options.add_experimental_option("detach", True)
	browser = webdriver.Chrome(chrome_options=chrome_options)
	browser.get(websiteName)

def getResults(keyWord):
	results = wikipedia.summary(keyWord, sentences=2)
	return results

def playSongs(songName):
	chrome_options = Options()
	chrome_options.add_experimental_option("detach", True)
	browser = webdriver.Chrome(chrome_options=chrome_options)

	songName = 'song ' + songName
	results = []
	for url in search(songName, stop=5):
		if url.find('youtube.com') >= 0:
			results.append(url)
	browser.get(results[1])

def getWeather():
	weather = 'weather'
	results = []
	for url in search(weather, stop=5):
		results.append(url)
	browser = webdriver.PhantomJS()

	browser.get(results[1])
	value = browser.find_element_by_class_name('/html/body/div[8]/div/div[10]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div[1]/div[1]/div/div[1]/span[1]')
	return str(value.text)

def getTime():
	time = datetime.now()
	hours = time.strftime('%I')
	mins = time.strftime('%M')
	pMaM = time.strftime('%p')
	return hours, mins, pMaM

def getDate():
	date = datetime.now()
	day = date.strftime('%A')
	dat = date.strftime('%d')
	month = date.strftime('%B')
	year = date.strftime('%Y')
	return day, dat, month, year

def getNews():
	main_url = 'https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=4dbc17e007ab436fb66416009dfb59a8'
	open_bbc_website = requests.get(main_url).json()
	article = open_bbc_website["articles"]

	result = []
	for articles in article:
		result.append(articles['title'])
	return result

def getStockPrices(stockName):
	stockPrice = yf.Ticker(stockName).info['ask']
	stockPrice = round(stockPrice, 1)
	return stockPrice