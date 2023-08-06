import hashlib
import time


class WaitForPageLoad(object):
    """
    This class is designed to be used with a "while" loop since it utilizes __enter__
    and __exit__ magic methods.

    The purpose of this class is to wait until the html of a page (as known by a
    Selenium WebDriver object) has changed.  The method of comparison is to check a
    before and after md5sum of the page source.

    The purpose of this is to add a layer of protection against the framework operating
    too quickly and .click() commands being issued to objects that still exist on a page
    before the browser has had the chance to actually load new content (which happens
    frequently).

    Core idea and code skeleton stolen from (except for the hashlib.md5 comparison):
    https://www.develves.net/blogs/asd/2017-03-04-selenium-waiting-for-page-load/
    """

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = hashlib.md5(self.browser.page_source.encode('utf-8')).hexdigest()

    def __exit__(self, *_):
        self.wait_for(self.page_has_loaded)

    @staticmethod
    def wait_for(condition_function):
        condition_met = False

        end_time = time.time() + 30
        while time.time() < end_time:
            if condition_function():
                condition_met = True
                break
            else:
                time.sleep(0.1)

        return condition_met

    def page_has_loaded(self):
        new_page = hashlib.md5(self.browser.page_source.encode('utf-8')).hexdigest()
        return new_page != self.old_page
