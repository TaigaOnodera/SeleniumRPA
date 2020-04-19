#coding: utf-8

import unittest, time, sys, re, requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

CHROME_DRIVER_PATH = '/bin/'

LINE_Notify_URL = 'https://notify-api.line.me/api/notify'
ACCESS_TOKEN = 'S1Vl8SdQGDbgS8m5ytMAmyWn4jQlYbFplv5ULWRgCyC'

GRAY_URL = 'https://www.amazon.co.jp/Nintendo-Switch-%E3%83%8B%E3%83%B3%E3%83%86%E3%83%B3%E3%83%89%E3%83%BC%E3%82%B9%E3%82%A4%E3%83%83%E3%83%81-Joy-%E3%83%90%E3%83%83%E3%83%86%E3%83%AA%E3%83%BC%E6%8C%81%E7%B6%9A%E6%99%82%E9%96%93%E3%81%8C%E9%95%B7%E3%81%8F%E3%81%AA%E3%81%A3%E3%81%9F%E3%83%A2%E3%83%87%E3%83%AB/dp/B07WS7BZYF/ref=sr_1_3?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=Nintendo+Switch+%E6%9C%AC%E4%BD%93+%28%E3%83%8B%E3%83%B3%E3%83%86%E3%83%B3%E3%83%89%E3%83%BC%E3%82%B9%E3%82%A4%E3%83%83%E3%83%81%29&qid=1586953706&s=videogames&sr=1-3'

COLORFUL_URL = 'https://www.amazon.co.jp/Nintendo-Switch-%E3%83%8B%E3%83%B3%E3%83%86%E3%83%B3%E3%83%89%E3%83%BC%E3%82%B9%E3%82%A4%E3%83%83%E3%83%81-%E3%83%8D%E3%82%AA%E3%83%B3%E3%83%96%E3%83%AB%E3%83%BC-%E3%83%90%E3%83%83%E3%83%86%E3%83%AA%E3%83%BC%E6%8C%81%E7%B6%9A%E6%99%82%E9%96%93%E3%81%8C%E9%95%B7%E3%81%8F%E3%81%AA%E3%81%A3%E3%81%9F%E3%83%A2%E3%83%87%E3%83%AB/dp/B07WXL5YPW/ref=sr_1_10?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=Nintendo+Switch+%E6%9C%AC%E4%BD%93+%28%E3%83%8B%E3%83%B3%E3%83%86%E3%83%B3%E3%83%89%E3%83%BC%E3%82%B9%E3%82%A4%E3%83%83%E3%83%81%29&qid=1586953706&s=videogames&sr=1-10'

DOUMORI_URL = 'https://www.amazon.co.jp/%E4%BB%BB%E5%A4%A9%E5%A0%82-Nintendo-Switch-%E3%81%82%E3%81%A4%E3%81%BE%E3%82%8C-%E3%81%A9%E3%81%86%E3%81%B6%E3%81%A4%E3%81%AE%E6%A3%AE%E3%82%BB%E3%83%83%E3%83%88/dp/B084HPMVNN/ref=sr_1_4?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=Nintendo+Switch+%E6%9C%AC%E4%BD%93+%28%E3%83%8B%E3%83%B3%E3%83%86%E3%83%B3%E3%83%89%E3%83%BC%E3%82%B9%E3%82%A4%E3%83%83%E3%83%81%29&qid=1586953706&s=videogames&sr=1-4'

LIMIT_VALUE_NORMAL  = 34000
LIMIT_VALUE_DOUMORI = 40000

# 送信用関数
def send2LINE(message, token):
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.post(LINE_Notify_URL, headers=headers, params=payload,)

# 値段を見る関数
def recogPrice(webdriver,URL,lim_value):
    webdriver.get(URL) # URLを開く
    test_value=0       # lim_valueとの比較用の変数
    txt=""             # カートボタンのテキスト部分
    price=""           # LINE送信用の値段表記
    
    # テキスト取得
    try:
        txt = webdriver.find_element_by_id('buyNew_noncbb').text         # 「カートに入れる」ボタンの場合
    except NoSuchElementException:
        try:
            txt = webdriver.find_element_by_id('unqualifiedBuyBox').text # 「すべての出品者を見る」ボタンの場合
        except :
            pass

    pattern = re.search('￥[0-9\,]*', txt) # txtから値段の書いてある部分を探す

    # 値段部分が見つかったら値段更新
    if pattern is not None:
        price = pattern.group()
        test_value = int(price[1:].replace(',',''))
    else:
        price = '取得できませんでした。'

    compare_result = test_value < lim_value

    # lim_value以下だったらLINEで送る
    if compare_result:
        itemName = webdriver.find_element_by_id('productTitle').text # 商品名を取得
        now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')           # 現在時刻も取得
        # 送信
        message = ('%s\n\n商品名 : %s\n\nURL: %s \n\n価格 : %s\n' %(now, itemName, URL, price))
        send2LINE(message, ACCESS_TOKEN)

    return not compare_result

if __name__ == '__main__':
    count = 0 # 今何分経ったかをカウントする変数
    # ブラウザの起動
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1280,1024')
        b = webdriver.Chrome(options=options,executable_path=CHROME_DRIVER_PATH+'chromedriver')
    except Exception as e:
        tb = sys.exc_info()[2]
        send2LINE("message:{0}".format(e.with_traceback(tb)), ACCESS_TOKEN)
        exit()

    # 値段確認ループ
    while True:
        # 全体で何かしらのエラーをキャッチさせる
        try:
            # 値段確認
            gray    = recogPrice(b, GRAY_URL    , LIMIT_VALUE_NORMAL )
            color   = recogPrice(b, COLORFUL_URL, LIMIT_VALUE_NORMAL )
            doumori = recogPrice(b, DOUMORI_URL , LIMIT_VALUE_DOUMORI)

            # １時間ほどで異常なければ定期連絡
            if gray and color and doumori and count%120 == 0:
                count = 0 # カウントリセット
                message = datetime.now().strftime("\n%m/%d %H:%M") + "\nNothing for alert" # LINE Notifyで送るメッセージ
                send2LINE(message, ACCESS_TOKEN)

            count = count+1
            time.sleep(30)

        except Exception as e:
            tb = sys.exc_info()[2]
            send2LINE("message:{0}".format(e.with_traceback(tb)), ACCESS_TOKEN)
            continue

