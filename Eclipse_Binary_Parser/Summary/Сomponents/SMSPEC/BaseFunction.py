import pandas as pd


class SMSPECHelper:

    @staticmethod
    def get_unsmry_link(link) -> str:
        ind = link.rindex('.')
        return link[:ind] + '.UNSMRY'

    @staticmethod
    def get_target_name(data: dict) -> list or None:
        if 'WGNAMES' in data and 'NAMES' not in data:
            return ['WGNAMES', 'KEYWORDS', 'NUMS', 'UNITS']
        elif 'NAMES' in data and 'WGNAMES' not in data:
            return ['NAMES', 'KEYWORDS', 'NUMS', 'UNITS']
        else:
            return None

    @staticmethod
    def get_type_keyword(storage: pd.DataFrame) -> tuple:
        if 'WGNAMES' in storage:
            return 'WGNAMES', 'KEYWORDS', 'NUMS', 'UNITS'
        elif 'NAMES' in storage:
            return 'NAMES', 'KEYWORDS', 'NUMS', 'UNITS'

