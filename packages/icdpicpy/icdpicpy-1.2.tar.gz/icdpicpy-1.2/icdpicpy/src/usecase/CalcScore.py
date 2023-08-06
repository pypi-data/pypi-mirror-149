import logging
import re
from typing import Optional

import pandas as pd

from icdpicpy.src.datamodel import Constants, Table, Score
from icdpicpy.src.datamodel.CodeMappingMethod import ICD10CodeMappingMethod, ISSCalcMethod
from icdpicpy.src.repository.DataRepository import DataRepository


class CalcScore:
    def __init__(self, data_repo: DataRepository):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__data_repo = data_repo

    def execute(self, patient_code_dict: dict, score_list: list = None, use_icd10: bool = True,
                icd10_method: str = 'gem_max', iss_calc_method: int = 1) -> Optional[pd.DataFrame]:
        self.__logger.debug(
            f'execute for {len(patient_code_dict)} patients, scores {score_list}, use_icd10: {use_icd10},'
            f' icd10 method: {icd10_method}, iss calculation method:{iss_calc_method}')

        if not self.__validate_params(patient_code_dict, use_icd10, icd10_method, iss_calc_method, score_list):
            return
        if score_list is None:
            score_list = Score.all_scores
        iss_calc_method = ISSCalcMethod.from_int(iss_calc_method)
        severity_data_df = self.__data_repo.read_data_file(Table.SeverityMap.file_name)
        if use_icd10:
            severity_data_df = self.__calc_icd10_severity(patient_code_dict, severity_data_df, icd10_method)
        res_df = None
        if severity_data_df is not None and Score.ISS_score in score_list:
            patient_iss_df = self.__calc_iss(patient_code_dict, severity_data_df, iss_calc_method)
            res_df = patient_iss_df
        if severity_data_df  is not None and Score.NISS_score in score_list:
            patient_niss_df = self.__calc_niss(patient_code_dict, severity_data_df, iss_calc_method)
            res_df = patient_niss_df if res_df is None else \
                res_df.merge(patient_niss_df, on=Table.Result.patient)
        if Score.Injury_cause in score_list:
            injury_cause_df = self.__data_repo.read_data_file(Table.InjuryCause.i9_file_name, sep='\t')
            if use_icd10:
                injury_cause_icd10_df = self.__data_repo.read_data_file(Table.InjuryCause.i10_file_name, sep='\t')
                injury_cause_df = pd.concat([injury_cause_df, injury_cause_icd10_df])

            patient_injury_cause_df = self.__get_injury_cause(patient_code_dict, injury_cause_df)
            if patient_injury_cause_df is not None:
                res_df = patient_injury_cause_df if res_df is None else \
                    res_df.merge(patient_injury_cause_df, on=Table.Result.patient)
        return res_df

    def __calc_iss(self, patient_code_dict: dict, severity_df: pd.DataFrame,
                   iss_calc_method: ISSCalcMethod) -> pd.DataFrame:
        self.__logger.debug('calc ISS')
        res = {Table.Result.patient: [], Table.Result.iss: []}
        for patient, codes in patient_code_dict.items():
            codes = [self.__prepare_code(c) for c in codes]
            # get only codes of the current patient
            curr_severity_df = severity_df[severity_df[Table.SeverityMap.code].isin(codes)]
            # severity score of 9 implies unknown severity.
            # Thus we want to exclude these as long as there is at least one known severity for the body region
            # However if all severity scores for the body region are 9 then we will assign max value of 9
            for br in curr_severity_df[Table.BaseColumns.issbr].unique():
                unique_values = curr_severity_df[Table.BaseColumns.severity].unique()
                if len(unique_values) > 1 and Constants.UnknownSeverityValue in unique_values:
                    # there are other values so Unknown can be removed
                    known_values_cond = (curr_severity_df[Table.BaseColumns.issbr] != br) | \
                                        (curr_severity_df[Table.BaseColumns.severity] != Constants.UnknownSeverityValue)
                    curr_severity_df = curr_severity_df.loc[known_values_cond, :]
            # find max severity for each body region
            br_df = curr_severity_df.groupby([Table.BaseColumns.issbr])[Table.BaseColumns.severity].max()
            # find iss as a sum of square of the largest severity scores but 75 is max
            severity_values: list = br_df.reset_index()[Table.BaseColumns.severity].tolist()
            severity_values.sort(reverse=True)
            max_pos = min(3, len(severity_values))
            severity_values = severity_values[:max_pos]
            if all([x == Constants.UnknownSeverityValue for x in severity_values]):
                iss_value = 'NA'
            else:
                severity_values = [0 if x == Constants.UnknownSeverityValue else x
                                   for x in severity_values]
                sqr_sum = 0
                if Constants.SeverityMaxValue in severity_values:
                    if iss_calc_method == ISSCalcMethod.default:
                        sqr_sum = Constants.MaxISSValue
                    elif iss_calc_method == ISSCalcMethod.extreme_cut:
                        severity_values = [x - 1 if x == Constants.MaxISSValue else x
                                           for x in severity_values]
                        sqr_sum = sum([x * x for x in severity_values])
                else:
                    sqr_sum = sum([x * x for x in severity_values])
                iss_value = min(sqr_sum, Constants.MaxISSValue)
            res[Table.Result.patient].append(patient)
            res[Table.Result.iss].append(iss_value)
        res_df = pd.DataFrame.from_dict(res)
        return res_df

    def __calc_niss(self, patient_code_dict: dict, severity_df: pd.DataFrame,
                    iss_calc_method: ISSCalcMethod) -> pd.DataFrame:
        self.__logger.debug('calc NISS')
        res = {Table.Result.patient: [], Table.Result.niss: []}
        for patient, codes in patient_code_dict.items():
            codes = [self.__prepare_code(c) for c in codes]
            # get only codes of the current patient
            severity_values = severity_df.loc[severity_df[Table.SeverityMap.code].isin(codes),
                                              Table.SeverityMap.severity].tolist()
            # severity score of 9 implies unknown severity.
            # Thus we want to exclude these as long as there is at least one known severity for the patient
            # However if all severity scores for the patient are 9 then we will assign value NA
            if all([x == Constants.UnknownSeverityValue for x in severity_values]):
                niss_value = 'NA'
            else:
                severity_values = [0 if x == Constants.UnknownSeverityValue else x
                                   for x in severity_values]
                severity_values.sort(reverse=True)
                max_pos = min(3, len(severity_values))
                severity_values = severity_values[:max_pos]
                if iss_calc_method == ISSCalcMethod.default:
                    if any([x == Constants.SeverityMaxValue for x in severity_values]):
                        niss_value = Constants.MaxISSValue
                    else:
                        niss_value = sum([x * x for x in severity_values])
                elif iss_calc_method == ISSCalcMethod.extreme_cut:
                    severity_values = [x - 1 if x == Constants.SeverityMaxValue else x
                                       for x in severity_values]
                    niss_value = sum([x * x for x in severity_values])
                else:
                    niss_value = 0
                niss_value = min(niss_value, Constants.MaxISSValue)

            res[Table.Result.patient].append(patient)
            res[Table.Result.niss].append(niss_value)

        res_df = pd.DataFrame.from_dict(res)
        return res_df

    def __prepare_code(self, code: str) -> str:
        code = code.strip().replace(".", "")
        if len(code) > 5 and code[5] == "X":
            return code[:5]
        if len(code) > 6 and code[6] == "X":
            return code[:6]
        return code

    def __validate_params(self, patient_code_dict: dict, use_icd10: bool, icd10_method: str,
                          iss_calc_method: int, score_list: Optional[list]) -> bool:
        self.__logger.debug('validate parameters')
        if not patient_code_dict:
            self.__logger.error(f'No patient data')
            return False

        if use_icd10 and ICD10CodeMappingMethod.from_string(icd10_method) is None:
            self.__logger.error(f'Unknown ICD10 mapping method {icd10_method}. '
                                f'Value should be one of {ICD10CodeMappingMethod.all_values()}')
            return False
        if ISSCalcMethod.from_int(iss_calc_method) is None:
            self.__logger.error(f'Unknown ISS calculation method {iss_calc_method}. '
                                f'Value should be one of {ISSCalcMethod.all_values()}')
            return False
        if score_list is not None:
            if any([x not in Score.all_scores for x in score_list]):
                self.__logger.error(f'Unknown score: {[x for x in score_list if x not in Score.all_scores]}. '
                                    f'Score can be one of {Score.all_scores}')
                return False
        return True

    def __get_injury_cause(self, patient_code_dict: dict, injury_cause_df: pd.DataFrame) -> Optional[pd.DataFrame]:
        self.__logger.debug('get injury cause')
        injury_cause_df[Table.InjuryCause.code] = injury_cause_df[Table.InjuryCause.code].apply(lambda x: x.strip())

        res = {Table.Result.patient: list(patient_code_dict.keys()),
               Table.Result.mechanism: [], Table.Result.intention: []}
        for p, codes in patient_code_dict.items():
            codes = [self.__prepare_code(c) for c in codes]
            mechanism, intention = self.__get_mechanism_and_intention(codes, injury_cause_df)
            res[Table.Result.mechanism].append(mechanism)
            res[Table.Result.intention].append(intention)
        return pd.DataFrame(data=res)

    def __get_mechanism_and_intention(self, codes: list, injury_cause_df: pd.DataFrame) -> tuple:
        self.__logger.debug(f'get mechanism and intention for {codes}')
        res = []
        for c in codes:
            # match by first 3 character to cut the most variants
            curr_df = injury_cause_df[injury_cause_df[Table.InjuryCause.code].str[:3] == c[:3]]
            # substitute 'X' in the end of a code on '*' for regex
            curr_df[Table.InjuryCause.code] = curr_df[Table.InjuryCause.code].apply(
                lambda x: f'{x[:-1]}.*' if x[-1] == 'X' else x
            )
            # substitute 'X' in the middle of a code on '(.)' for regex
            curr_df[Table.InjuryCause.code] = curr_df[Table.InjuryCause.code].apply(
                lambda x: f'{x[:x.rfind("X")]}(.){x[x.rfind("X") + 1:]}' if x.rfind('X') > 0 else x
            )
            # match codes
            match = curr_df[Table.InjuryCause.code].apply(lambda x: re.search(x, c) is not None)
            curr_df = curr_df[match]
            if curr_df.empty:
                continue
            curr_df[Table.InjuryCause.code] = c
            curr_df[Table.InjuryCause.mechanism] = curr_df. \
                groupby([Table.InjuryCause.code, Table.InjuryCause.intention])[Table.InjuryCause.mechanism]. \
                transform(lambda x: '/'.join(x))
            curr_df = curr_df.drop_duplicates()
            res.append(curr_df)
        mechanism = ''
        intention = ''
        if res:
            df = pd.concat(res)
            if not df.empty:
                mechanism = '/'.join(df[Table.InjuryCause.mechanism].unique().tolist())
                intention = '/'.join(df[Table.InjuryCause.intention].unique().tolist())
        return mechanism, intention

    def __calc_icd10_severity(self, patient_code_dict: dict, severity_data_df: pd.DataFrame,
                              icd10_method: str) -> Optional[pd.DataFrame]:
        self.__logger.debug('calc icd10 severity')
        icd10_icd9_map_df = self.__data_repo.read_data_file(Table.Icd10Icd9Map.file_name)
        all_codes = [item for _, values in patient_code_dict.items() for item in values]
        all_codes = [self.__prepare_code(x) for x in all_codes]
        icd10_icd9_map_df = icd10_icd9_map_df[icd10_icd9_map_df[Table.Icd10Icd9Map.icd10].isin(all_codes)]
        # map icd10 on severity
        merged_severity_data_df = severity_data_df.merge(icd10_icd9_map_df,
                                                         left_on=Table.SeverityMap.code,
                                                         right_on=Table.Icd10Icd9Map.icd9)
        i10_severity_df = merged_severity_data_df[[Table.Icd10Icd9Map.icd10, Table.SeverityMap.severity,
                                                   Table.SeverityMap.issbr]]
        i10_severity_df = i10_severity_df.rename({Table.Icd10Icd9Map.icd10: Table.SeverityMap.code}, axis=1)
        # concat icd 9 and icd10 severity tables
        severity_data_df = pd.concat([severity_data_df, i10_severity_df])
        severity_data_df = severity_data_df[severity_data_df[Table.SeverityMap.code].isin(all_codes)]
        # resolve mapping conflict according to icd10_method
        method = ICD10CodeMappingMethod.from_string(icd10_method)
        if method is None:
            self.__logger.error(f'Unknown ICD10 mapping method {icd10_method}')
        if method == ICD10CodeMappingMethod.gem_min:
            agg_function = 'min'
        elif method == ICD10CodeMappingMethod.gem_max:
            agg_function = 'max'
        else:
            self.__logger.error(f'Unknown icd10 mapping method {icd10_method}')
            return None
        severity_data_df[Table.SeverityMap.severity] = \
            severity_data_df.groupby([Table.SeverityMap.code])[Table.SeverityMap.severity].transform(agg_function)
        severity_data_df = severity_data_df.drop_duplicates()
        return severity_data_df
