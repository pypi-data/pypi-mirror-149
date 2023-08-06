""" ./core/automancy_chain.py """
from selenium.webdriver.common.action_chains import ActionChains as SeleniumActionChains


class AutomancyChain(SeleniumActionChains):
    """
    This is a workaround override for the core Selenium ActionChains class required to support
    action_chain functionality in SafariDriver relating to the 'pause' method used within the
    'move_to_element' method (amongst others).

    The exact problem was reported here along with this solution.

    https://stackoverflow.com/questions/52947603/selenium-action-move-to-element-doesnt-work-in-safari-because-of-usupported

    """
    # TODO -> Revisit this issue periodically. Comment out the override after Selenium/SafariDriver are updated and retest for the failure.
    def __init__(self, driver):
        super(AutomancyChain, self).__init__(driver)
        if driver.name in ('Safari', 'Safari Technology Preview'):
            self.w3c_actions.key_action.pause = lambda *a, **k: None
