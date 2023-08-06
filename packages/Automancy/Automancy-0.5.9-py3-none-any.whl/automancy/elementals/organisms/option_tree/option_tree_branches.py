""" ./elementals/organisms/calendar/option_tree_branches.py """
from .option_tree_branch import OptionTreeBranch


class OptionTreeBranches(object):
    """ Container for the options in an Option Tree (as properties """
    def __init__(self):
        self.ordered_options = []

    def __contains__(self, item):
        return item in self.ordered_options

    def __getitem__(self, item):
        if type(item) is str and hasattr(self, item):
            return getattr(self, item)
        else:
            return None

    def __len__(self):
        branch_count = 0
        properties = dir(self)

        for own_property in properties:
            if type(getattr(self, own_property)) == OptionTreeBranch:
                branch_count += 1

        return branch_count

    def add(self, branch):
        """
        Adds a OptionTreeBranch object to self as a class property while also adding a reference to the
        name of the branch to the self.ordered_options list

        Args:
            branch (OptionTreeBranch): A single branch that should be added as a property to this object

        Returns:
            None

        """
        setattr(self, branch.label, branch)

        if branch.label not in self.ordered_options:
            self.ordered_options.append(branch.label)

    def remove(self, branch_name):
        """
        Removes a branch from self and deletes the reference to the branch in the ordered list of options

        Args:
            branch_name (str): Name of the option we want to remove from self.

        Returns:
            None

        """
        if hasattr(self, branch_name):
            # Delete the property from self
            delattr(self, branch_name)

            # Delete the option from the ordered list of options.
            for index, option_name in enumerate(self.ordered_options):
                if branch_name == option_name:
                    del(self.ordered_options[index])
