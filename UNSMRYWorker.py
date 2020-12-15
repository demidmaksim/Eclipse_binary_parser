from BinaryWorker import *


class UNSMRYLoader(BinaryWorker):
    def __init__(self, link):
        super().__init__(link)
        self.results: Content or None = None
        self.dimension: tuple or None = None
        self.loaded = 0

    def _add_data(self, content: Content) -> None:
        if self.results is None:
            value = content.value
            content.value = np.zeros(self.dimension) * np.nan
            content.value[self.loaded, :] = value
            self.results = content
        else:
            value = content.value
            self.results.value[self.loaded, :] = value
        self.loaded += 1

    def load(self, main_dimension: tuple,
             start: np.array, length: np.array) -> np.ndarray:
        self.dimension = (main_dimension[0], sum(length))
        self.reading_definite_part('PARAMS', start, length)
        return self.results.value


class UNSMRYWorker:
    def __init__(self, link: str, dimension: tuple):
        self.link: str = link
        self.dimension: tuple = dimension

    def get_data_from_file(self, start: np.ndarray,
                           length: np.ndarray) -> np.ndarray:
        loader = UNSMRYLoader(self.link)
        return loader.load(self.dimension, start, length)