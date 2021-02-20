import numpy as np


class SUMMARY:
    def __init__(self, position_matrix: list, data: list or np.array):
        self.position_matrix: list = position_matrix
        self.data: list or np.array = data

    def report(self):
        for point in self.position_matrix:
            point(f'Name: {point[0]}\t'
                  f'KeyWord: {point[1]}\t'
                  f'Num: {point[2]}')

    def get(self, names: str or list, keywords: str or list,
            nums: int or list) -> list or None:

        if type(names) == list:
            results = []
            for name_id, name in enumerate(names):
                keyword = keywords[name_id]
                num = nums[name_id]

                try:
                    ind = self.position_matrix.index([name, keyword, num])
                except ValueError:
                    print("NO VALUE!")
                    return None

                results.append(self.data[ind])
                return results
        else:

            try:
                ind = self.position_matrix.index([names, keywords, nums])
            except ValueError:
                print("NO VALUE!")
                return None

            return self.data[ind]
