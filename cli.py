import os
import wget
import time
import click

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options



def load_driver(binary_location='./Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary',
                executable_path='/usr/local/Cellar/chromedriver/2.37/bin/chromedriver'):
    options = Options()
    options.binary_location = binary_location
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path=executable_path)
    return driver

def get_images(driver):
    return driver.find_elements_by_css_selector('.container.maincontents .slider img')

def current_page(driver):
    return int(driver.find_elements_by_css_selector('.pagination li.active a')[0].get_attribute('value'))

def pages_num(driver):
    return len(driver.find_elements_by_css_selector('.pagination li'))

def get_nextpage(driver):
    page = current_page(driver)
    pages_count = len(driver.find_elements_by_css_selector('.pagination li'))
    if page < pages_count:
        return page + 1
    return None

def download_image(url, dest_dir, page, idx):
    filename = '{}-{}.jpg'.format(page, idx)
    fp = os.path.join(dest_dir, filename)
    print(fp)
    # wget.download(url, out=dest_dir)
    # try:
    #     data = urllib.request.urlopen(url).read()
    #     with open(fp, mode="wb") as f:
    #         f.write(data)
    # except urllib.error.URLError as e:
    #     print(e)

def crawl_page(driver, url, dest_dir, page=1, timeout=10):
    target_url = '{}&paged={}'.format(url, page)
    driver.get(target_url)
    sleep_count = 0
    while not get_images(driver):
        sleep_count += 1
        time.sleep(1)
        print('waiting...')
        if sleep_count > timeout:
            driver.save_screenshot('error-screen.png')
            raise Exception('Time out')
    page = current_page(driver)
    for idx, img_tag in enumerate(get_images(driver)):
        image_url = img_tag.get_attribute('src')
        download_image(image_url, dest_dir, page, idx)
    next_page = get_nextpage(driver)
    if next_page:
        crawl_page(driver, url, dest_dir, page=next_page)

@click.command()
@click.argument('url')
def command(url):
    driver = load_driver()
    print("Chrome Browser Initialized in Headless Mode")
    dest_dir = os.path.join(os.path.dirname(__file__), 'images')
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    crawl_page(driver, url, dest_dir)
    driver.quit()

if __name__ == '__main__':
    command()
