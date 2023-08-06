""" Support for a modal element and it's components """
from automancy.core import AutomancyChain, Elemental, Model


class Modal(Elemental, Model):
    def __init__(self, locator, human_name, system_name):
        Elemental.__init__(self, locator, human_name, system_name)
        Model.__init__(self)
        self.close_button = None
        self.cancel_button = None
        self.confirm_button = None
        self.title = None

    @property
    def position(self):
        return

    def confirm(self) -> None:
        """ Clicks the button that is generally thought of as 'accept' or 'ok' or 'save', etc"""
        if self.confirm_button:
            self.confirm_button.click()

    def cancel(self) -> None:
        """ Clicks the button that is generally thought of as 'cancel' """

    def close(self) -> None:
        """ Clicks the X button that modals tend to have at the top right of their boundaries to close it """
        if self.close_button:
            self.close_button.click()

    def dismiss(self) -> None:
        """ Finds a location outside the boundaries of the modal and clicks it in order to dismiss the modal """
        # Find a target point beyond the boundaries of the modal to click on.
        target_offset_x = ((self.width / 2) * -1) - 10

        actions = AutomancyChain(self.browser)
        actions.move_to_element(self.element())
        actions.move_by_offset(target_offset_x, 0)
        actions.click()
        actions.perform()
