""" ./decorators/interaction.py """
import time

from functools import wraps

from selenium.common.exceptions import NoSuchElementException, \
    StaleElementReferenceException, ElementNotVisibleException


def interaction(wrapped_function):
    """
    This is a decorator function that can prefix other methods in this class.

    The intent of this decorator is that it should be used above methods that will
    "interact" with page elements that might have become stale.

    If a Selenium WebElement is detected as stale, this decorator method refreshes
    the instantiated class's assigned element property object so that the element
    can be interacted with again.

    This is necessary in some instances when page changes happen too rapidly and
    page elements are attempted to be interacted with before they're technically
    ready.

    A part of the process in refreshing the element object is that WebDriverWait
    is called again in order to make sure that the element is available again.

    This was first introduced once it became apparent that elements that were
    needed existed on a page and would be collected within a larger page object
    but then the page would be modified and the sub elements would lose their
    associations, requiring them to be refreshed.

    I seriously hate explicit calls for manual page elements refreshes...
    That shit should happen automatically...
    """

    def wrapper(*args, **kwargs):

        try:
            work = wrapped_function(*args, **kwargs)
        except StaleElementReferenceException:
            args[0].refresh()
            work = wrapped_function(*args, **kwargs)
        except NoSuchElementException:
            args[0].refresh()
            work = wrapped_function(*args, **kwargs)
        except ElementNotVisibleException:
            time.sleep(1)
            args[0].refresh()
            work = wrapped_function(*args, **kwargs)
        return work

    return wraps(wrapped_function)(wrapper)
