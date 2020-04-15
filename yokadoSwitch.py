#!/usr/bin/python

import unittest, time
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

driver = webdriver.Chrome("/bin/chromedriver")
class TestHoge(unittest.TestCase):

    RETRIES = 3
    TIMEOUT = 10

    """初期化"""
    def setUp(self):
        self.browser = Browser()

    """テスト終了"""
    def tearDown(self):
        self.browser.quitBrowser()

    """PCサイト"""
    def testPcSite(self):
        # ブラウザ起動
        self.browser.openChrome()
        driver = self.browser.driver
        driver.maximize_window()  # 最大化
        driver.implicitly_wait(2) # 暗黙の待機(2秒)

        # ページの読み込み待ち時間(10秒)
        driver.set_page_load_timeout(self.TIMEOUT)

        i = 0
        while i < self.RETRIES:
            try:
                driver.get("https://google.co.jp/")
                time.sleep(5)

            except TimeoutException:
                i = i + 1
                print("Timeout, Retrying... (%(i)s/%(max)s)" % {'i': i, 'max': self.RETRIES})
                continue

            else:
                return True

        msg = "Page was not loaded in time(%(second)s sec)." % {'second': self.TIMEOUT}
        raise TimeoutException(msg)


##### MAIN #####
if __name__ == "__main__":
    unittest.main()
