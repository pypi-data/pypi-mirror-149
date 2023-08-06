import logging
import os
from typing import Optional

import pandas as pd

from icdpicpy.src.datamodel import Table


class DataRepository:
    def __init__(self):
        self.__logger = logging.getLogger(self.__class__.__name__)

    def read_patient_data_file(self, file_name: str) -> Optional[dict]:
        self.__logger.debug(f'read patient data file : {file_name}')
        if not os.path.exists(file_name):
            self.__logger.error(f'can not find file : {file_name}')
            return None
        with open(file_name) as f:
            lines = f.readlines()
        lines = [line.split(',') for line in lines]
        patient_code_dict = {line[0]: line[1:] for line in lines}
        self.__logger.debug(f'read {len(patient_code_dict)} patients')
        return patient_code_dict

    def read_data_file(self, file_name: str, sep=',') -> Optional[pd.DataFrame]:
        self.__logger.debug(f'read file "{file_name}"')
        data_path = f'{os.path.dirname(__file__)}/../../data'
        file_name = f'{data_path}/{file_name}'
        if not os.path.exists(file_name):
            self.__logger.error(f'can not find file : {file_name}')
            return None
        try:
            df = pd.read_csv(file_name, sep=sep)
            if Table.BaseColumns.code in df.columns:
                df[Table.BaseColumns.code] = df[Table.BaseColumns.code].astype(str)
            return df
        except Exception as e:
            self.__logger.error(e)
            return None

    def save_df(self, df: pd.DataFrame, file_name: str):
        df.to_csv(file_name, index=False)
