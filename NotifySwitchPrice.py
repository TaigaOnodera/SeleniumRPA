#coding: utf-8

import unittest, time, sys, re, requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

LINE_Notify_URL = "https://notify-api.line.me/api/notify"
ACCESS_TOKEN = 'S1Vl8SdQGDbgS8m5ytMAmyWn4jQlYbFplv5ULWRgCyC'

GRAY_URL = 'https://www.amazon.co.jp/Nintendo-Switch-%E3%83%8B%E3%83%B3%E3%83%86%E3%83%B3%E3%83%89%E3%83%BC%E3%82%B9%E3%82%A4%E3%83%83%E3%83%81-Joy-%E3%83%90%E3%83%83%E3%83%86%E3%83%AA%E3%83%BC%E6%8C%81%E7%B6%9A%E6%99%82%E9%96%93%E3%81%8C%E9%95%B7%E3%81%8F%E3%81%AA%E3%81%A3%E3%81%9F%E3%83%A2%E3%83%87%E3%83%AB/dp/B07WS7BZYF/ref=sr_1_3?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=Nintendo+Switch+%E6%9C%AC%E4%BD%93+%28%E3%83%8B%E3%83%B3%E3%83%86%E3%83%B3%E3%83%89%E3%83%BC%E3%82%B9%E3%82%A4%E3%83%83%E3%83%81%29&qid=1586953706&s=videogames&sr=1-3'

COLORFUL_URL = 'https://www.amazon.co.jp/Nintendo-Switch-%E3%83%8B%E3%83%B3%E3%83%86%E3%83%B3%E3%83%89%E3%83%BC%E3%82%B9%E3%82%A4%E3%83%83%E3%83%81-%E3%83%8D%E3%82%AA%E3%83%B3%E3%83%96%E3%83%AB%E3%83%BC-%E3%83%90%E3%83%83%E3%83%86%E3%83%AA%E3%83%BC%E6%8C%81%E7%B6%9A%E6%99%82%E9%96%93%E3%81%8C%E9%95%B7%E3%81%8F%E3%81%AA%E3%81%A3%E3%81%9F%E3%83%A2%E3%83%87%E3%83%AB/dp/B07WXL5YPW/ref=sr_1_10?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=Nintendo+Switch+%E6%9C%AC%E4%BD%93+%28%E3%83%8B%E3%83%B3%E3%83%86%E3%83%B3%E3%83%89%E3%83%BC%E3%82%B9%E3%82%A4%E3%83%83%E3%83%81%29&qid=1586953706&s=videogames&sr=1-10'

DOUMORI_URL = 'https://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-Nintendo-Switch-%E3%81%82%E3%81%A4%E3%81%BE%E3%82%8C-%E3%81%A9%E3%81%86%E3%81%B6%E3%81%A4%E3%81%AE%E6%A3%AE%E3%82%BB%E3%83%83%E3%83%88/dp/B084HPMVNN/ref=sr_1_4?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=Nintendo+Switch+%E6%9C%AC%E4%BD%93+%28%E3%83%8B%E3%83%B3%E3%83%86%E3%83%B3%E3%83%89%E3%83%BC%E3%82%B9%E3%82%A4%E3%83%83%E3%83%81%29&qid=1586953706&s=videogames&sr=1-4'

LIMIT_VALUE = 34000

def recogPrice(webdriver,URL,lim_value):
	# URLを開く
	webdriver.get(URL)
	# lim_valueとの比較用の変数 
	# 0にしておけばとりあえず比較はしてくれるし、異常の通知になるかも？
	test_value = 0;

	# 値段を取得
	try:
		# 「カートに入れる」ボタンの場合
		price = webdriver.find_element_by_id('buyNew_noncbb').text
	except NoSuchElementException:
		# 「すべての出品者を見る」ボタンの場合
		price = webdriver.find_element_by_id('unqualifiedBuyBox').text
	
	# 空文字じゃなければ
	if price:
		price = re.search('￥[0-9\,]*', price).group()
		test_value = int(price[1:].replace(",",""))
	else:
		price = price + "(取得できませんでした。)"

	# lim_value以下だったらLINEで送る
	if test_value< lim_value:
		# 商品名を取得
		itemName = webdriver.find_element_by_id('productTitle').text
		# 現在時刻も取得
		now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		# LINE Notifyで送るメッセージ
		message = ("%s\n\n商品名 : %s\n\nURL: %s \n\n価格 : %s\n"%(now, itemName, URL, price))
		payload = {'message': message}
		
		# 送信処理
		headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}
		r = requests.post(LINE_Notify_URL, headers=headers, params=payload,)
		#一応PCにも表示
		print(message)

if __name__ == '__main__':

	# ブラウザの起動とログイン
	try:
		b = webdriver.Chrome('/bin/chromedriver')
	except:
		l('Failed to open browser.')
		exit()

	# 値段確認ループ
	while True:
		# 値段確認
		recogPrice(b,GRAY_URL, LIMIT_VALUE)
		recogPrice(b,COLORFUL_URL, LIMIT_VALUE)
		recogPrice(b,DOUMORI_URL, 40000)

		time.sleep(60)

	
