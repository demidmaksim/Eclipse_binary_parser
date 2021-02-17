import os
from .Сomponents.Content import *


class BinarySave:
    def __init__(self):
        pass


class BinaryReader:
    def __init__(self, link: str):
        self.link: str = link
        self.data = dict()
        self.__HeadConst = HeaderConstructor()
        self.__ContConst = ContentConstructor()

    def _add_data(self, content: Content) -> None:
        if content.header.keyword in self.data.keys():
            self.data[content.header.keyword].add_simple_value(content.value)
        else:
            self.data[content.header.keyword] = content

    def reload_data(self) -> None:
        self.data = dict()

    def reading_all_file(self) -> None:
        self.reload_data()
        with open(self.link, 'rb') as file:
            while file.tell() < os.path.getsize(self.link):
                header = self.__HeadConst.from_file(file)
                content = self.__ContConst.from_file(header, file, mode='all')
                self._add_data(content)

    def reading_definite_part(self, keyword: str,
                              start_reading: np.array,
                              len_reading: np.array) -> None:
        self.reload_data()
        with open(self.link, 'rb') as file:
            loaded = 0
            while file.tell() < os.path.getsize(self.link):
                loaded += 1
                header = self.__HeadConst.from_file(file)
                header.set_limitation(start_reading, len_reading)
                if keyword == header.keyword:
                    content = self.__ContConst.from_file(header, file,
                                                         mode='definite')
                    self._add_data(content)
                else:
                    self.__ContConst.skip_all_block(header, file)
