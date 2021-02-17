from Eclipse_Binary_Parser.Summary.Сomponents.SMSPEC.SMSPECWorker import *
from Eclipse_Binary_Parser.Summary.Сomponents.UNSMRY.UNSMRYLoader import *


class SUMMARYWorker:

    def __init__(self, smspec_link: str):
        self.SMSPEC = SMSPECWorkerConstructor.from_file(smspec_link)
        self.UNSMRY = UNSMRYLoader(smspec_link.replace('SMSPEC', 'UNSMRY'))

    def __get_dimension(self, names: str or list):
        time_length = self.SMSPEC.time.get_number_of_step()
        if type(names) == list:
            name_length = len(names)
        else:
            name_length = 1
        return time_length, name_length

    def get(self, names: str or list, keywords: str or list, nums: str or list):
        start, length = self.SMSPEC.get_read_vector(names, keywords, nums)
        dimension = self.__get_dimension(names)
        results = self.UNSMRY.get_from_file(start, length, dimension)
        return results



"""
class SUMMARYHelper:

    @staticmethod
    def get_unsmry_link(smspec_link: str) -> str:
        ind = smspec_link.rindex('.')
        return smspec_link[:ind] + '.UNSMRY'

    @staticmethod
    def get_key(name: str, keyword: str, num: int) -> str:
        return f'{name}/{keyword}/{str(num)}'



    def get_key_list(self, position: list) -> list:
        position.sort()
        key_list = list()
        for point in position:
            key = self.get_key(point[1], point[2], point[3])
            key_list.append(key)
        return key_list


class SUMMARYDownloader(SUMMARYHelper):
    def __init__(self, smspecworker: SMSPECWorker, unsmryworker: UNSMRYWorker):
        self.SMSPECWorker = smspecworker
        self.UNSMRYWorker = unsmryworker

    @staticmethod
    def __check_correct(names: list, keywords: list, nums: list) -> bool:
        len_names = len(names)
        len_keywords = len(keywords)
        len_nums = len(nums)
        if len_names == len_keywords and len_nums == len_keywords:
            return True
        else:
            return False

    def __get_positions(self, names: list,
                        keywords: list, nums: list) -> list:
        positions = list()
        if self.__check_correct(names, keywords, nums):
            for name_id, name in enumerate(names):
                keyword = keywords[name_id]
                num = nums[name_id]
                position = self.SMSPECWorker.get_position(name, keyword, num)
                positions.append([position, name, keyword, num])
        return positions

    def __get_what_must_download(self, df: pd.DataFrame, names: list,
                                 keywords: list, nums: list) -> tuple:
        md_names = []           # Names for Must download
        md_keywords = []        # Keywords for Must download
        md_nums = []            # Nums for Must download
        for name_id,  name in enumerate(names):
            key = self.get_key(name, keywords[name_id], nums[name_id])
            if key not in df.keys():
                md_names.append(name)
                md_keywords.append(keywords[name_id])
                md_nums.append(nums[name_id])
        return md_names, md_keywords, md_nums

    def must_download(self, df: pd.DataFrame,
                      names: list,
                      keywords: list,
                      nums: list) -> pd.DataFrame or None:
        must_download = self.__get_what_must_download(df, names,
                                                      keywords, nums)

        if must_download[0]:
            md_names = must_download[0]
            md_keywords = must_download[1]
            md_nums = must_download[2]
            return self.__download(md_names, md_keywords, md_nums)
        else:
            return None

    def __download(self, names: list, keywords: list,
                   nums: list) -> pd.DataFrame:
        positions = self.__get_positions(names, keywords, nums)
        names_key = self.get_key_list(positions)
        start, length = self.structuring(positions)
        np_matrix = self.UNSMRYWorker.get_data_from_file(start, length)
        return pd.DataFrame(data=np_matrix, columns=names_key)


class SummarySave:
    def __init__(self):
        pass


class SUMMARYWorker(SUMMARYHelper):
    def __init__(self, link: str):
        self.SMSPECWorker = None
        self.UNSMRYWorker = None
        self.__initialization(link)
        self.df = pd.DataFrame()

    def __initialization(self, link: str) -> None:
        unsmrylink = self.get_unsmry_link(link)
        self.SMSPECWorker = SMSPECWorker(link)
        dimension = self.SMSPECWorker.dimension
        self.UNSMRYWorker = UNSMRYWorker(unsmrylink, dimension)

    def __get_data(self, names: list, keywords: list,
                   nums: list) -> pd.DataFrame:
        get_df = pd.DataFrame()
        for name_id, name in enumerate(names):
            key = self.get_key(name, keywords[name_id], nums[name_id])
            get_df[key] = self.df[key]
        return get_df

    def __add_data(self, df: pd.DataFrame) -> None:
        self.df = pd.concat([self.df, df], axis=1)

    def get_all_data(self) -> pd.DataFrame:
        return self.df

    def add_data(self,  names: list, keywords: list, nums: list) -> None:
        loader = SUMMARYDownloader(self.SMSPECWorker, self.UNSMRYWorker)
        additional_df = loader.must_download(self.df, names, keywords, nums)

        if additional_df is not None:
            self.__add_data(additional_df)

    def get_data(self, names: list, keywords: list, nums: list) -> pd.DataFrame:
        self.add_data(names, keywords, nums)
        return self.__get_data(names, keywords, nums)

    def clear_data_frame(self) -> None:
        self.df = pd.DataFrame()

    def report(self):
        print(f'SMSPECWorker: {list(self.SMSPECWorker.data.keys())}')
        print(f'KEYWORDS: '
              f'{list(pd.unique(self.SMSPECWorker.storage["KEYWORDS"]))}')
        print(f'WGNAMES: '
              f'{list(pd.unique(self.SMSPECWorker.storage["WGNAMES"]))}')


class SummaryConstructor:
    def __init__(self):
        pass

    @staticmethod
    def open_file(link: str) -> SUMMARYWorker:
        return SUMMARYWorker(link)

    @staticmethod
    def check_keyword(data: dict):
        target_keyword = [
            'KEYWORDS',
            'NAMES',
            'NUMS',
            'UNITS',
            'STARTDAT'
        ]
        for key in data.keys():
            if key not in target_keyword:
                return False
        return True

    @staticmethod
    def create_units(keywords: list) -> list:
        df = pd.read_csv('Сomponents/UNSMRY/keyword.txt', sep='\t', index_col=None)
        df.replace(np.nan, '', inplace=True)
        units = list()
        for keyword in keywords:
            unit = df[df['KEYWORD'] == keyword]['UNITS']
            if unit.values[0]:
                unit = unit.values[0]
            else:
                unit = ''
            units.append(unit)
        return units

    @staticmethod
    def __get_datatype(keyword):
        if keyword in ['KEYWORDS', 'WGNAMES', 'NAMES', 'UNITS', 'RESTART']:
            return 'CHAR'
        elif keyword in ['NUMS', 'STARTDAT', 'SEQHDR', 'MINISTEP', 'DIMENS']:
            return 'INTE'
        elif keyword in ['PARAMS']:
            return 'REAL'

    @staticmethod
    def create_content(data: dict, key: str):
        head_const = HeaderConstructor()
        cont_const = ContentConstructor()
        num_of_objects = len(data[key])
        datatype = SummaryConstructor.__get_datatype(key)
        header = head_const.from_variable(key, num_of_objects, datatype)
        return cont_const.from_variable(header, data[key])

    @staticmethod
    def create_bytes_string(data: dict):
        bytes_list = list()
        for key in data.keys():
            content = SummaryConstructor.create_content(data, key)
            bytes_list.append(content.to_bytes())
        return b''.join(bytes_list)

    @staticmethod
    def __add_in_unsmry_file(link: str, data: dict):
        data['SEQHDR'] = [0]
        data['MINISTEP'] = [0]
        data_for_save = SummaryConstructor.create_bytes_string(data)
        with open(link, 'ab+') as file:
            file.write(data_for_save)

    @staticmethod
    def create_smspec_file(link: str, data: dict):
        data_for_save = SummaryConstructor.create_bytes_string(data)
        with open(link, 'wb') as file:
            file.write(data_for_save)
"""