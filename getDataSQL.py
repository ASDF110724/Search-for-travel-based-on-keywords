import pandas as pd
import pymysql
import os
import sys


# sql로 불러오기
def findDataBySQL():
    """
    1. sql에 연결하고
    2. 테이블 places에 있는 컬럼 place_id, place_name를 모두 조회
    3. 조회한 데이터를 한줄씩 분리
    4. 한줄씩 반복해서 리스트로 저장
    5. id, name 리스트를 각각 반환
    """

    # sql 연결
    conn = pymysql.connect(
        host="",
        user="",
        password="",
        db="",
        charset="",
    )
    # 커서 생성
    cur = conn.cursor()

    # 테이블 places에 있는 컬럼 place_id, place_name를 모두 조회
    cur.execute("SELECT place_id,place_name FROM places")

    # 위에서 조회한 데이터를 한줄씩 분리해 저장
    row = cur.fetchall()

    # 분해한 데이터를 한줄씩 반복 저장한 칼럼이 [id , name] 형태이기 때문에 첫번째 인덱스인 'name'을 호출
    name_list = [name[1] for name in row]
    # print("name_list : ", name_list)
    id_list = [id[0] for id in row]
    # print("id_list : ", id_list)

    # sql 저장 후 종료
    conn.commit()
    conn.close()

    # 데이터를 2개 반환 (다른 언어는 함수에서 데이터 1개만 반환 가능하다고 합니다.)
    return id_list, name_list


def findKeyword():
    """
    1. sql 연결
    2. word에 있는 값을 모두 리스트화시켜 저장
    3. word 리스트를 반환
    """
    # sql 연결
    conn = pymysql.connect(
        host="",
        user="",
        password="",
        db="",
        charset="",
    )

    # 커서 생성
    cur = conn.cursor()

    # word에 있는 값을 모두 리스트화시켜 저장
    cur.execute("SELECT word From keywords")
    keywords_values = [row[0] for row in cur.fetchall()]

    conn.commit()
    conn.close()
    return keywords_values


def insertKeywordBySQL(values):
    """
    1. sql 연결
    2. keywords에 values 값을 삽입
    """
    # sql 연결
    conn = pymysql.connect(
        host="",
        user="",
        password="",
        db="",
        charset="",
    )

    # 커서 생성
    cur = conn.cursor()
    # keywords에 values 값을 삽입
    cur.execute("INSERT INTO keywords (word) VALUES(%s)", values)

    # sql 저장 후 종료
    conn.commit()
    conn.close()


# a, b = findDataBySQL()
# print("a : ", a)
# print("b : ", b)


def getKeywordID(keyword):
    """
    1. sql 연결
    2. keyword에 해당하는 ID 조회
    3. 변수 keywordID에 위에서 찾은 ID입력
    4. keywordID를 반환
    """
    # sql 연결
    conn = pymysql.connect(
        host="",
        user="",
        password="",
        db="",
        charset="",
    )

    # 커서 생성
    cur = conn.cursor()

    # keyword에 해당하는 ID 조회
    cur.execute("SELECT keyword_id FROM keywords WHERE word = %s", keyword)

    # keywordID에 해당하는 ID를 넣고
    keywordID = cur.fetchone()

    conn.commit()
    conn.close()

    # 해당 값을 반환
    return keywordID


def inputNewID(placeID, keywordID):
    """
    1. sql 연결
    2. places_keywords안에 있는 place_id ,keyword_id를 입력한다
    """
    # sql 연결
    conn = pymysql.connect(
        host="",
        user="",
        password="",
        db="",
        charset="",
    )

    # 커서 생성
    cur = conn.cursor()

    # places_keywords안에 있는 place_id ,keyword_id를 변수를 받아 입력한다
    cur.execute(
        "INSERT INTO places_keywords (place_id, keyword_id ) VALUES(%s, %s)",
        (placeID, keywordID),
    )
    conn.commit()
    conn.close()
