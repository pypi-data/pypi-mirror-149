from typing import Optional

from icdpicpy.src.Application import Application
from icdpicpy.src.datamodel.CodeMappingMethod import ICD10CodeMappingMethod, ISSCalcMethod


def calc_score(data: Optional[dict] = None, source_file: Optional[str] = None,
               res_file: Optional[str] = None, score_list: Optional[list] = None, use_icd10: bool = True,
               icd10_method: str = ICD10CodeMappingMethod.gem_max.value,
               iss_calc_method: int = ISSCalcMethod.default.value):
    app = Application()
    return app.calc_score(data, source_file, res_file, score_list, use_icd10, icd10_method, iss_calc_method)
