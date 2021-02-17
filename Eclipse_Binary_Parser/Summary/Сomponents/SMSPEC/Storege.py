
class Storage:
    def __init__(self):
        pass


class SMSPECIndexator(SMSPECHelper):

    @staticmethod
    def __get_num_pattern(storage: pd.DataFrame,
                          num: int or None) -> pd.DataFrame():
        if num is not None:
            return storage['NUMS'] == num
        else:
            return storage['NUMS'] == storage['NUMS']

    @staticmethod
    def get_position(storage: pd.DataFrame, name: str,
                     keyword: str, num: int = None) -> int:
        type_key = SMSPECIndexator.get_type_keyword(storage)
        name_pattern = storage[type_key[0]] == name
        keyword_pattern = storage['KEYWORDS'] == keyword
        num_pattern = SMSPECIndexator.__get_num_pattern(storage, num)
        loaded_pattern = storage['LOADED'] == False
        pattern = name_pattern & keyword_pattern & num_pattern & loaded_pattern
        return storage[pattern].index[0]

