import time
import re, csv
from random import uniform, randint

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class HeadlessBrowser(object):
    def __init__(self, attacker=None, driver_path=None, browser_path=None):
        self.attach = attacker
        self.driver = self.load_driver(executable_path=driver_path, binary_location=browser_path)

    def load_driver(self, binary_location=None, executable_path=None):
        options = Options()
        options.binary_location = binary_location
        options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options, executable_path=executable_path)
        return driver

    def request(self, url):
        self.driver.get(url)

    def wait_parse(self, parser, sleep_time=1, timeout=10):
        sleep_count = 0
        images = parser(self.driver)
        while not images:
            sleep_count += 1
            time.sleep(sleep_time)
            print('waiting...')
            if sleep_count == timeout:
                success = self.attach(self.driver)
                if success:
                    sleep_count = 0
            if sleep_count > timeout:
                self.driver.save_screenshot('../error-screen.png')
                raise Exception('Time out')
            images = parser(self.driver)
            self.driver.save_screenshot('../error-screen.png')
        return images

    def get_next_page(self, pagination_parser):
        current_page = pagination_parser.get_current_page(self.driver)
        pages = pagination_parser.get_pages(self.driver)
        if current_page >= pages:
            raise Exception('Next page does not exist.')
        return current_page + 1

    def stop_crawl(self):
        self.driver.quit()
