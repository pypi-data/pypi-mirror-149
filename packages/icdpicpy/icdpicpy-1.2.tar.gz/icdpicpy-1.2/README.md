# ICDPICPY

International Classification of Diseases Programs for Injury Categorization in Python

The ICDPICPY package is a partial implementation of the R program ICDPICR (https://github.com/ablack3/icdpicr) in Python.

The icd9 code severity (Abbreviated Injury Scale) and body region is calculated according to the table from ICDPIC.
To obtain icd10 severity and body region, icd10 codes is mapped to icd9 with GEM map version of 2018 and then severity score calculated by ICDPIC table.

To resolve GEM mapping conflicts, where one icd10 mapped to several icd9 with different severity values, two methods were implemented:
- gem-min: takes code with minimal severity
- gem-max: takes code with maximal severity

Injury mechanism and intention is taken from CDC mapping files

Sources:
External cause of injury: 
https://www.cdc.gov/nchs/injury/injury_tools.htm

General Equivalence Mappings:
https://www.cms.gov/Medicare/Coding/ICD10/2018-ICD-10-PCS-and-GEMs

Severity mapping, ICDPICR:
https://github.com/ablack3/icdpicr