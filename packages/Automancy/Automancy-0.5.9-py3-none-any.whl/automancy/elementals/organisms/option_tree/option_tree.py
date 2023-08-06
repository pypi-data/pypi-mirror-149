""" ./elementals/organisms/calendar/option_tree.py """
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as wait
from selenium.webdriver.support.ui import WebDriverWait

from automancy.core import Elemental

from .option_tree_branch import OptionTreeBranch
from .option_tree_branches import OptionTreeBranches


class OptionTree(Elemental):
    """ Organism OptionTree used for elements that present a tree of options and option branches for the user. """
    def __init__(self, locator: str, human_name: str, system_name: str, collapser_type=None, collapser_locator='', selector_type=None, selector_locator=''):
        """
        Notes:
            Options sometimes are collapsible so sometimes have a collapse_button_locator to be defined.

        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name
            collapser_type (any): Optional: A Elemental based class such as Button
            collapser_locator (str): Optional: A string which represents the xpath locator for the collapser object
            selector_type (any): Optional: A Elemental based class such as Checkbox or Radio
            selector_locator (str): Optional: A string which represents the xpath locator for the selector object

        """
        super().__init__(locator, human_name, system_name)
        self.branches = OptionTreeBranches()
        self.branch_locator = ''

        # Used when branches can be collapsed, type is usually going to be of type Button
        self.collapsible_branches = False
        self.collapser_locator = collapser_locator
        self.collapser_type = collapser_type

        if collapser_type:
            self.collapsible_branches = True

        # Used as an alternative selection method such as Checkbox or Radio
        self.selector_locator = selector_locator
        self.selector_type = selector_type

    def get_branches(self):
        """
        Looks for the elements that match the branch locator string (returns a list)
        Once found, iterates through each WebElement and construct an OptionTreeBranch
        for each found.  Append each to the instance "branches" list.

        Returns:
            None

        """

        if self.branch_locator:
            branches = WebDriverWait(self.browser, 30).until(wait.presence_of_all_elements_located((By.XPATH, self.branch_locator)))

            if branches:
                for index, branch in enumerate(branches):
                    # Define the branch name and locator used in creating the Elemental.
                    branch_num = index + 1
                    branch_name = branch.text
                    branch_locator = '({locator})[{index}]'.format(locator=self.branch_locator, index=branch_num)

                    # Create the OptionTreeBranch Elemental
                    branch = OptionTreeBranch(branch_locator + self.selector_locator, 'Option Tree Branch', 'branch')

                    branch.selector = self.define_branch_selector(branch_locator, branch_name)
                    branch.locator = self.define_selector_locator(branch_locator)

                    branch.collapser = self.define_branch_collapser(branch_locator, branch_name)

                    # Add the branch to the instance branches property
                    self.branches.add(branch)

    def define_branch_selector(self, branch_locator, branch_name):
        if self.selector_type and self.selector_locator:
            return self.selector_type(self.define_selector_locator(branch_locator), name=branch_name)

    def define_branch_collapser(self, branch_locator, branch_name):
        if self.collapser_type and self.selector_locator:
            collapser_locator = '{branch}{collapser_locator}'.format(branch=branch_locator, collapser_locator=self.collapser_locator)
            return self.collapser_type(collapser_locator, name=branch_name)

    def define_selector_locator(self, branch_locator):
        return '{branch}{special_locator}'.format(branch=branch_locator, special_locator=self.selector_locator)

    def select(self, option_name):
        """
        Selects an option tree branch based on the name of the option
        if the option name exists as a property within self.branches.

        Args:
            option_name (str): The name of the

        Returns:
            None

        """
        if type(option_name) is str and option_name in self.branches:
            self.branches[option_name].click()
