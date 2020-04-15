import unittest, time
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

LOGIN_ID = 'monnhannyarouze@gmail.com'
LOGIN_PASSWORD = 'Imokuwanaito8'

TIMEOUT = 10
ITEM_URL = 'https://7net.omni7.jp/detail/1107087574'

LIMIT_VALUE = 3000

def l(str):
	print("%s : %s"%(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),str))

if __name__ == '__main__':
	# ブラウザの起動
	try:
		b = webdriver.Chrome('/bin/chromedriver')
		b.get(ITEM_URL)
		# ページの読み込み待ち時間(10秒)
		b.set_page_load_timeout(TIMEOUT)
	except:
		l('Failed to open browser.')
		exit()

	# ログイン処理を最初に行うようにしたい 今後の課題
	#try:
		#b.find_element_by_id('ap_email').send_keys(LOGIN_ID)
		#b.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
		#b.find_element_by_id('signInSubmit').click()
	#except:
		#l('LOGIN PASS.')
		#pass

	atag=None
	# 商品ページを開くまでのループ
	while True:
		# タイムアウト
		try:
			b.get(ITEM_URL)
			time.sleep(TIMEOUT)
		except TimeoutException:
			print("Timeout, Retrying...")
			continue
		else:
			# 予約ボタンの要素を取得
			try:
				atag=b.find_element_by_class_name("js-pressTwice")
			except NoSuchElementException:
				l("this element is not found.")
				continue
				#sys.exit(1)
			break

	# 予約完了までのループ
	while True:
		# CTRLボタンを押下しながらクリックすることで, 新規タブでカートを開く
		ActionChains(b).move_to_element(atag).key_down(Keys.CONTROL).click().key_up(Keys.CONTROL).perform()

		# ここでカートページへの遷移を期待
		cartTab = b.window_handles[1]
		b.switch_to_window(cartTab)
		try:
			time.sleep(TIMEOUT)	
		# もしタイムアウトしてしまったらタブ削除して商品ページから再スタート
		except TimeoutException:
			print("Timeout, Retrying...")
			b.close()
			continue
		
		# カートページにいけたら注文手続きボタンを押す
		try:
			b.find_element_by_id("orderProcessing").click()
		except NoSuchElementException:
			l("this element is not found.")
			sys.exit(1)

		# ここで注文確定ページへの遷移を期待
		try:
			time.sleep(TIMEOUT)	
		# もしタイムアウトしてしまったらタブ削除して商品ページから再スタート
		except TimeoutException:
			print("Timeout, Retrying...")
			b.close()
			continue

		# 注文確認ページにいけたら注文確定ボタンを押す
		try:
			b.find_element_by_id("orderProcessing").click()
		except NoSuchElementException:
			l("this element is not found.")
			sys.exit(1)
	l('ALL DONE.')
