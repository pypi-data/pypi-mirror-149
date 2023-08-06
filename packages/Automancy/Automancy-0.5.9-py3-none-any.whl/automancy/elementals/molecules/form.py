""" ./elementals/molecules/form.py """
from automancy.core import Elemental, Model


class Form(Elemental, Model):
    """ Organism Form for collections of smaller Elemental that make up a form (inputs, labels, buttons) """
    def __init__(self, locator: str, human_name: str, system_name: str):
        """
        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name

        """
        Elemental.__init__(self, locator, human_name, system_name)
        Model.__init__(self)
        self.submit = None
        self.text_inputs = {}
