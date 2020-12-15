from BinaryWorker import *
import pandas as pd
import datetime as dt


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


class TimeConstructor(SMSPECHelper):

    @staticmethod
    def get_datetime(start_date: dt.datetime, days: float) -> dt.datetime:
        return start_date + dt.timedelta(days=days)

    @staticmethod
    def convert_to_datetime(start_date: dt.datetime,
                            dey_vector: list or np.ndarray) -> list:
        return [TimeConstructor.get_datetime(start_date, i) for i in dey_vector]

    @staticmethod
    def get_start_time(data: dict) -> dt.datetime:
        start_date = data['STARTDAT'].value
        day = start_date[0]
        month = start_date[1]
        year = start_date[2]
        hour = start_date[3]
        minute = start_date[4]
        second = int(start_date[5])
        start_date = dt.datetime(year, month, day, hour, minute, second)
        return start_date

    @staticmethod
    def get_time_vec(link: str, storage: pd.DataFrame) -> np.ndarray:
        unsmry_link = SMSPECHelper.get_unsmry_link(link)
        unsmry_worker = BinaryWorker(unsmry_link)
        start = np.array([SMSPECIndexator.get_position(storage, '', 'TIME', 0)])
        length = np.array([1])
        unsmry_worker.reading_definite_part('PARAMS', start, length)
        time_model = np.array(unsmry_worker.data['PARAMS'].value)
        time_model = time_model.T[0]
        return time_model


class SMSPECWorker(BinaryWorker):
    def __init__(self, link):
        super().__init__(link)
        self.__initialization()

    def __get_dimension(self) -> None:
        number_of_step = len(self.dey_vector)
        number_of_word = len(self.data['KEYWORDS'].value)
        self.dimension = (number_of_step, number_of_word)

    def __create_data_frame(self) -> None:
        self.reading_all_file()
        target_name = SMSPECHelper.get_target_name(self.data)
        dict_for_df = dict.fromkeys(target_name)
        for key in dict_for_df:
            if key in self.data.keys():
                dict_for_df[key] = list(self.data[key].value)
        self.storage = pd.DataFrame.from_dict(dict_for_df)
        bool_vector = [False for _ in range(self.storage.shape[0])]
        self.storage['LOADED'] = bool_vector

    def __initialization(self) -> None:
        self.__create_data_frame()
        self.start_date = TimeConstructor.get_start_time(self.data)
        self.dey_vector = TimeConstructor.get_time_vec(self.link, self.storage)
        self.dt_vector = TimeConstructor.convert_to_datetime(self.start_date,
                                                             self.dey_vector)
        self.__get_dimension()

    def get_position(self, name: str, keyword: str, num: int = None) -> int:
        return SMSPECIndexator.get_position(self.storage, name, keyword, num)
