import logging
import os.path
from logging import config
from typing import Optional

import pandas as pd
from icdpicpy.src.datamodel.CodeMappingMethod import ICD10CodeMappingMethod, ISSCalcMethod

from icdpicpy.src.repository.DataRepository import DataRepository
from icdpicpy.src.usecase.CalcScore import CalcScore


class Application:
    __log_config_path = f"{os.path.dirname(__file__)}/../config/logging.conf"

    def __init__(self):
        self.__init_logging()
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__data_repo = DataRepository()

    def calc_score(self, data: Optional[dict] = None, source_file: Optional[str] = None,
                   res_file: Optional[str] = None, score_list: Optional[list] = None, use_icd10: bool = True,
                   icd10_method: str = ICD10CodeMappingMethod.gem_max,
                   iss_calc_method: int = ISSCalcMethod.default) -> Optional[pd.DataFrame]:
        self.__logger.debug('calc score')
        if data is None and source_file is None:
            self.__logger.error("No data was passed")
            return None
        if data is None:
            data = self.__data_repo.read_patient_data_file(source_file)
        res_df = CalcScore(self.__data_repo).execute(data, score_list, use_icd10, icd10_method, iss_calc_method)
        if res_file and res_df is not None:
            self.__data_repo.save_df(res_df, res_file)
        return res_df

    def __init_logging(self):
        print(self.__log_config_path)
        logging.config.fileConfig(self.__log_config_path)
