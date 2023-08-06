""" ./core/browser.py """
import inspect


class Browser(object):
    def __init__(self):
        self.driver = Browser.find_driver()
        self.name = self.driver.capabilities['browserName']

    @staticmethod
    def __search_in_frame_locals(frame):
        """
        Does the work of searching through the first layer of the frame stack for Elemental.find_browser()

        Args:
            frame ():

        Returns:

        """
        browser = None

        if 'browser' in frame[0].f_locals and frame[0].f_locals['browser']:
            browser = frame[0].f_locals['browser']

        elif 'driver' in frame[0].f_locals and frame[0].f_locals['driver']:
            browser = frame[0].f_locals['driver']

        return browser

    @staticmethod
    def __get_driver_identifier(frame_locals):
        """
        Determines how the Selenium webdriver is named in frame_locals.

        Either 'driver' or 'browser'.  Does not inspect for any other variations.

        Args:
            frame_locals (Any): the locals of a stack frame

        Returns:
            str: Either 'driver' or 'browser' as the identifier of the Selenium webdriver object.

        """
        identifier = ''
        if 'driver' in frame_locals:
            identifier = 'driver'
        elif 'browser' in frame_locals:
            identifier = 'browser'

        return identifier

    @staticmethod
    def __search_in_frame_stack(frame):
        """
        Extension method to Elemental.__search_in_frame_locals(...) as a fail over.

        If a search through f_locals object for the frame doesn't contain the WebDriver object, this method is
        called in order to search the stack within that frame for it (which is where it generally is).

        This method is only called when a Elemental subclass is instantiated below the highest level of
        the hierarchy when authoring tests which is sometimes done.

        In a sense, this is a fallback method if a test or subsequent test helper isn't written ideally.

        :param frame: Python frame stack object
        :type frame:
        :return: The Selenium WebDriver object
        :rtype: None, WebDriver
        """
        browser = None
        frame_locals = frame[0].f_locals
        driver_identifier = Browser.__get_driver_identifier(frame_locals)

        if driver_identifier in frame_locals and not frame_locals[driver_identifier] and 'stack' in frame_locals:
            for subframe in frame_locals['stack']:
                # Determine if the driver is in the current subframe
                driver_in_subframe = 'self' in subframe[0].f_locals and hasattr(subframe[0].f_locals['self'], driver_identifier)

                # If the driver identifier is in the subframe, get the attribute
                if driver_in_subframe:
                    browser = getattr(subframe[0].f_locals['self'], driver_identifier)

                # Stop the loop if 'browser" is not None (indicating that we've discovered the real object)
                if browser:
                    break

        return browser

    @staticmethod
    def find_driver():
        """
        Searches through Python process frames in order to implicitly find a reference for
        the Selenium WebDriver object.

        This is massively beneficial to the designed easy of authoring tests because it allows
        a test author to avoid explicitly passing the driver through every layer of the this
        framework (which is ugly and makes the process significantly more messy)

        :return: The Selenium WebDriver object
        :rtype: None, WebDriver
        """
        stack = inspect.stack()
        browser = None

        for frame in stack:
            browser = Browser.__search_in_frame_locals(frame)
            if browser:
                break
            else:
                browser = Browser.__search_in_frame_stack(frame)
                if browser:
                    break

        return browser

    def new_tab(self):
        """ Opens a new tab for the browser """
        self.driver.execute_script('window.open("");')
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def next_tab(self):
        """
        Switches the browser context to the next tab that's open.
        Opens a tab if there is only one tab open.
        Selenium does not have a better way of handling this need.
        For now each Elemental instance will have this ability.
        """
        # Create a new tab if there is only one open
        if len(self.driver.window_handles) == 1:
            self.new_tab()
            return

        # Get the current tab's window handle
        current_handle = self.driver.current_window_handle

        # If the current handle equals the last known window handler open we want to switch to the first handle created
        if current_handle == self.driver.window_handles[-1]:
            self.driver.switch_to.window(self.driver.window_handles[0])
        else:
            next_handle = self.driver.window_handles.index(current_handle)
            self.driver.switch_to.window(self.driver.window_handles[next_handle + 1])
