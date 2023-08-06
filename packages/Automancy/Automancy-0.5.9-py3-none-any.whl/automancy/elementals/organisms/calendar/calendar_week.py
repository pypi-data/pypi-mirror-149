""" ./elementals/organisms/calendar/calendar_week.py """
from automancy.core import Elemental


class CalendarWeek(Elemental):
    def __init__(self, locator: str, human_name: str, system_name: str):
        super().__init__(locator, human_name, system_name)
