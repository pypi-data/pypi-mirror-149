class BaseColumns:
    code = 'code'
    severity = 'severity'
    issbr = 'issbr'


class InjuryCause:
    i9_file_name = 'icd9_intention_cause.txt'
    i10_file_name = 'icd10_intention_cause.txt'
    intention = 'intention'
    mechanism = 'mechanism'
    code = 'code'


class SeverityMap:
    file_name = 'icd9_severity.csv'
    code = "code"
    severity = "severity"
    issbr = "issbr"


class Icd10Icd9Map:
    file_name = 'i10_i9_2018_gem.csv'
    icd10 = 'icd10'
    icd9 = 'icd9'


class Result:
    mortality = 'mortality'
    patient = 'patient'
    iss = 'ISS'
    niss = 'NISS'
    mechmaj = "mechmaj"
    mechmin = "mechmin"
    mechanism = "mechanism"
    intention = "intention"
