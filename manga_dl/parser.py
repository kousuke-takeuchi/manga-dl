class MangamuraParser(object):
    @classmethod
    def find_images(cls, driver):
        return driver.find_elements_by_css_selector('.container.maincontents .slider img')

    class Pagination(object):
        @classmethod
        def get_current_page(cls, driver):
            return int(driver.find_elements_by_css_selector('.pagination li.active a')[0].get_attribute('value'))

        @classmethod
        def get_pages(cls, driver):
            return len(driver.find_elements_by_css_selector('.pagination li'))
