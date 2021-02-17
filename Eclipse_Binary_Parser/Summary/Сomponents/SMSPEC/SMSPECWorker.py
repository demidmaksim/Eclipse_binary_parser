from Eclipse_Binary_Parser.BaseBinaryWorker.BinaryWorker import *
import pandas as pd


class SMSPECWorker(BinaryWorker):
    def __init__(self, link, ):
        super().__init__(link)
        self.dimension = None
        self.start_date = None
        self.dey_vector = None
        self.dt_vector = None
        self.storage = None

    def get_position(self, name: str, keyword: str, num: int = None) -> int:
        return SMSPECIndexator.get_position(self.storage, name, keyword, num)

    def get_list_position(self, names: list, keywords: list, nums: list) -> list:
        positions = list()
        for name_id, name in enumerate(names):
            keyword = keywords[name_id]
            num = nums[name_id]
            ind = SMSPECIndexator.get_position(self.storage, name, keyword, num)
            positions.append(ind)
        return positions


class SMSPECWorkerConstructor:

    @staticmethod
    def create(link) -> SMSPECWorker:
        smspec_work = SMSPECWorker(link)
        smspec_work.reading_all_file()
        storage = SMSPECWorkerConstructor.__create_data_frame(smspec_work.data)
        start_date, dey_v, dt_v = SMSPECWorkerConstructor.\
            __time_constructor(link, smspec_work.data, storage)
        dimension = SMSPECWorkerConstructor.__get_dimension(dey_v,
                                                            smspec_work.data)
        smspec_work.dimension = dimension
        smspec_work.start_date = start_date
        smspec_work.dey_vector = dey_v
        smspec_work.dt_vector = dt_v
        smspec_work.storage = storage
        return smspec_work

    @staticmethod
    def __get_dimension(dey_vector, data) -> tuple:
        number_of_step = len(dey_vector)
        number_of_word = len(data['KEYWORDS'].value)
        return number_of_step, number_of_word

    @staticmethod
    def __create_data_frame(data) -> pd.DataFrame:
        target_name = SMSPECHelper.get_target_name(data)
        dict_for_df = dict.fromkeys(target_name)
        for key in dict_for_df:
            if key in data.keys():
                dict_for_df[key] = list(data[key].value)
        storage = pd.DataFrame.from_dict(dict_for_df)
        bool_vector = [False for _ in range(storage.shape[0])]
        storage['LOADED'] = bool_vector
        return storage

    @staticmethod
    def __time_constructor(link, data, storage) -> tuple:
        start_date = TimeConstructor.get_start_time(data)
        dey_vector = TimeConstructor.get_time_vec(link, storage)
        dt_vector = TimeConstructor.convert_to_datetime(start_date, dey_vector)
        return start_date, dey_vector, dt_vector
