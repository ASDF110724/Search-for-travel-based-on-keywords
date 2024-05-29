# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---
# 작성한 함수들을 모두 받아서 실행시키는 메인 코드
import pandas as pd


from getKeywords import getKeywordFile
from getDataSQL import findDataBySQL
from insertDataFromSQL import *

# +
# main


def main():
    # palces에 있는 place_id, place_name을 각각 리스트로 입력받는 함수
    id_list, name_list = findDataBySQL()

    #
    # 키워드를 출력 (사용시 getKeywordFile 함수 슬라이싱 수정필요)
    getKeywordFile(id_list, name_list)
    # csv을 읽어와서
    file = pd.read_csv(
        filepath_or_buffer="C:/AICC_STUDY/Project_test_01/data/IDKeywordData.csv",
        encoding="cp949",
        names=["ID", "Name", "Keyword"],
        header=None,
    )

    # sql keywords에 동일 키워드 제거하고 입력하는 함수
    insertNewKeyword(file)

    # sql places_keywords에 place_id keyword_id 받아서 입력하는 함수
    getNewIDData(file)
    # -


if __name__ == "__main__":
    main()
