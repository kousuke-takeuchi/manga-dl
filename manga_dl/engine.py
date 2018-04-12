from .browser import HeadlessBrowser
from .dl import wget_image
from .recaptcha import brute_force_attach
from .parser import MangamuraParser


class MangamuraCrawler(object):
    def __init__(self, parameter, single=True, dest='../images', driver_path=None, browser_path=None):
        self.base_url = 'http://mangamura.org/old_viewer?p={}'
        self.parameter = parameter
        self.single = single
        options = {
            'attacker': brute_force_attach,
            'driver_path': driver_path,
            'browser_path': browser_path
        }
        print("Chrome Browser Initialized in Headless Mode")
        self.browser = HeadlessBrowser(**options)

    def crawl(self, page=1):
        # [TODO: タブ管理機能]
        # tab = self.browser.create_tab()
        # ↑ crawlerで各タブに対する司令を管理

        # 1. 漫画ページを読み込む
        url = self.base_url.format(page)
        self.browser.request(url)
        # 2. 画像のURLを取得
        # パーサーに定義されたタグが見つからない場合は
        # レンダリングされるまで待つ。レンダリングすらされない場合は
        # recaptchaが表示されているため、attackを内部で呼び出している
        images = self.browser.wait_parse(MangamuraParser.find_images)
        # 3. 取得した画像をダウンロード
        for image in images:
            wget_image(image, dest)
        # 4. 次のページへ
        try:
            next_page = self.browser.get_next_page(MangamuraParser.Pagination)
        except Exception:
            self.browser.stop_crawl()
        self.crawl(next_page)
