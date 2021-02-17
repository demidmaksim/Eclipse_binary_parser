import pandas as pd
import datetime as dt
import numpy as np
from Eclipse_Binary_Parser.BaseBinaryWorker.BinaryWorker import *




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
    def get_time_vec(link: str) -> np.ndarray:
        unsmry_link = SMSPECHelper.get_unsmry_link(link)
        unsmry = BinaryWorker(unsmry_link)
        unsmry.reading_definite_part('PARAMS', np.array([0]), np.array([1]))
        time_model = np.array(unsmry.data['PARAMS'].value)
        return time_model


class Time:
    def __init__(self, data):
        start_date = TimeConstructor.get_start_time(data)
        dey_vector = TimeConstructor.get_time_vec(link, storage)
        dt_vector = TimeConstructor.convert_to_datetime(start_date, dey_vector)
