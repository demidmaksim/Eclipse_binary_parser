from .Сomponents.SMSPEC.Reader.SMSPECReader import *
from .Сomponents.UNSMRY.UNSMRYLoader import *


class SUMMARYReader:

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
