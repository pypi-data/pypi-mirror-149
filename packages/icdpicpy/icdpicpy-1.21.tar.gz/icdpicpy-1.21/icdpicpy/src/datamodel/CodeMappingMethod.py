from __future__ import annotations

from enum import Enum
from typing import Optional

from icdpicpy.src.datamodel import Table


class ICD10CodeMappingMethod(Enum):
    # Method of ISS calculation for ICD10 code system
    # roc_max_NIS = 'roc_max_NIS'  # Table derived empirically from National Inpatient Sample (NIS) maximizing area under an ROC curve. For ICD10 codes not in NIS the mapping based on TQIP data will be used as a backup. This option is recommended if the user's data are similar to NIS data.
    # roc_max_TQIP = 'roc_max_TQIP'  # Table derived empirically from the Trauma Quality Improvement Program (TQIP) data maximizing area under an ROC curve. For ICD-10 codes not in TQIP the mapping based on NIS data will be used as a backup. This option is recommended if the user's data are similar to TQIP data.
    # roc_max_NIS_only = 'roc_max_NIS_only'  # Table derived as for "roc_max_NIS", but injury ICD-10 codes not in the NIS dataset will be ignored
    # roc_max_TQIP_only = 'roc_max_TQIP_only'  # Table derived as for "roc_max_TQIP", but injury ICD-10 codes not in the TQIP dataset will be ignored.
    gem_max = 'gem_max'  # Table derived by mapping ICD-10-CM to ICD-9-CM using the CMS general equivalence mapping tables and then to AIS and ISS using the ICDPIC table inherited from the Stata version.  Mapping conflicts handled by taking the max AIS.
    gem_min = 'gem_min'  # Same as "gem_max" except that mapping conflicts are handled by taking the min AIS.

    @classmethod
    def from_string(cls, method_name: str) -> Optional[ICD10CodeMappingMethod]:
        for x in ICD10CodeMappingMethod:
            if method_name == x.value:
                return x
        return None

    # @classmethod
    # def get_iss_column(cls, method: ICD10CodeMappingMethod) -> str:
    #     if method == ICD10CodeMappingMethod.roc_max_NIS:
    #         return Table.i10_map_roc.NIS_severity
    #     if method == ICD10CodeMappingMethod.roc_max_NIS_only:
    #         return Table.i10_map_roc.NIS_only_severity
    #     if method == ICD10CodeMappingMethod.roc_max_TQIP:
    #         return Table.i10_map_roc.TQIP_severity
    #     if method == ICD10CodeMappingMethod.roc_max_TQIP_only:
    #         return Table.i10_map_roc.TQIP_only_severity

    @classmethod
    def all_values(cls):
        return [x.value for x in ICD10CodeMappingMethod]


class ISSCalcMethod(Enum):
    default = 1  # will assign an ISS of 75 if any AIS is 6
    extreme_cut = 2  # will change any AIS = 6 to 5 and then calculate ISS normally

    @classmethod
    def from_int(cls, int_value: int) -> Optional[ISSCalcMethod]:
        for x in ISSCalcMethod:
            if int_value == x.value:
                return x
        return None

    @classmethod
    def all_values(cls):
        return "1 - assign an ISS of 75 if any AIS is 6; 2 - change any AIS = 6 to 5 and then calculate ISS normally"
