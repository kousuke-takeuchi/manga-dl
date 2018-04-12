import os
import click

from .engine import MangamuraCrawler


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


browser_path = os.path.join(BASE_DIR, '../Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary')
driver_path = '/usr/local/Cellar/chromedriver/2.37/bin/chromedriver'


@click.command()
@click.argument('p')
def command(p):
    dest = os.path.join(BASE_DIR, '../images')
    if not os.path.exists(dest):
        os.mkdir(dest)
    crawler = MangamuraCrawler(p, single=True, dest=dest, driver_path=driver_path, browser_path=browser_path)
    crawler.crawl()
