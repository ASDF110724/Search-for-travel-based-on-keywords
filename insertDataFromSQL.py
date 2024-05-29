import pandas as pd

import getDataSQL


def insertNewKeyword(csv_file):
    """
    1. csv파일을 읽어오고
    2. 해당 csv의 컬럼 'Keyword'를 불러와서 set(중복제거)
    3. sql에 접속해서 Keywords의 word를 모두 가져오고
    4. 불러온 word와 비교해서 Keyword에 없으면 word에 추가
    """
    # 2. csv의 컬럼 'Keyword'를 불러와서 set화(중복제거)
    Keyword_value = set(csv_file["Keyword"])

    # 3. sql에 접속해서 Keywords의 word를 모두 가져오고
    keywordData = getDataSQL.findKeyword()

    # 4. 불러온 word와 비교해서 Keyword에 없으면 word에 추가
    for i in Keyword_value:
        if i not in keywordData:
            # print("inputdata : ", i)
            getDataSQL.insertKeywordBySQL(i)


def getNewIDData(csv_file):
    """
    1. csv 파일을 받아서 한 행씩 반복
    2. sql에서 Keyword에 해당하는 keywordID를 조회
    3. placeID 와 keywordID 를 가져와 sql의 places_keywords에 삽입
    """

    csv_file.drop_duplicates(inplace=True)
    # 1. csv 파일을 받아서 한 행씩 반복
    for idx, row in csv_file.iterrows():
        # 2. sql에서 Keyword에 해당하는 keywordID를 조회
        keywordID = getDataSQL.getKeywordID(row["Keyword"])
        # 3. placeID 와 keywordID 를 가져와 sql의 places_keywords에 삽입
        getDataSQL.inputNewID(row["ID"], keywordID)
