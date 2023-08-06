from icdpicpy import Calculator


def main():
    Calculator.calc_score(
        source_file="C:\\Users\\kosta\\Documents\\Houston\\dev\\icdpicpy\\icdpicpy\\build\\test_iss.csv",
        res_file="C:\\Users\\kosta\\Documents\\Houston\\dev\\icdpicpy\\icdpicpy\\build\\res_iss.csv",
        # score_list=['ISSA'],
        # icd10_method='gem_min',
    )


if __name__ == '__main__':
    main()
