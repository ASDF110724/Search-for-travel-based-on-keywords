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

import requests
from bs4 import BeautifulSoup
import re
from konlpy.tag import Okt
from collections import Counter
import pandas as pd
import time

import getDataSQL


# 한글 아닌 것 공백으로 바꾸기
def text_cleaning(text):
    hangul = re.compile("[^ ㄱ-ㅣ가-힣]+")
    result = hangul.sub("", text)
    return result


# +
# 3-1. 한글 뽑기


def get_hangul(titleList):

    # 한글만 추출하기
    titleList = list(map(lambda x: text_cleaning(x), titleList))
    # print(titleList)

    title_corpus = " ".join(titleList)  # 추출한 각 요소를 띄어쓰기로 join
    nouns_tagger = Okt()  # 형태소 초기화
    nouns = nouns_tagger.nouns(title_corpus)  # 명사 추출

    count = Counter(nouns)  # 명사 갯수 세기\

    return count


# +
# 3-2.불용어 필터링


def get_stopwords(count):

    # 데이터 길이가 1보다 큰 것만 필터링
    remove_char_counter = Counter({x: count[x] for x in count if len(x) > 1})

    # 불용어 처리 경로 지정
    korean_stopwords_path = "C:/AICC_STUDY/Project_test_01/data/stopwords-ko.txt"

    # stopwords 파일 열기
    with open(korean_stopwords_path, encoding="utf8") as f:
        stopwords = f.readlines()
    stopwords = [x.strip() for x in stopwords]

    # 위에서 필터링한 리스트를 하나씩 for 문 돌려서 stopwords에 해당되지 않는 것만 갯수 세기
    remove_char_counter = Counter(
        {x: remove_char_counter[x] for x in remove_char_counter if x not in stopwords}
    )
    # print(remove_char_counter)

    return remove_char_counter


# +
# 3. 키워드 뽑기 (한글뽑기 + 불용어 필터링)


def get_keyword(titleList):

    hg = get_hangul(titleList)

    keyword = get_stopwords(hg)

    return keyword


# -


# 4. 키워드 저장
def trans_keywordList(remove_char_counter):

    ranked_tags = remove_char_counter.most_common(15)  # 빈도순 n개 단어
    # 딕셔너리로 변환
    ranked_tags = dict(ranked_tags)
    # 단어와 빈도를 dataframe으로 갖고오기
    df = pd.DataFrame(ranked_tags.items(), columns=["단어", "빈도"])
    # 빈도수 필터링
    words = list(df.loc[df["빈도"] > 24, "단어"])

    return words


# place_id, place_name,keyword 변수들을 받아 새로운 데이터프레임으로 만들어 반환
def rebornDataFrame(idn, names, words):
    word_len = len(words)

    #
    df = pd.DataFrame(
        [[str(idn)] * word_len, [names] * word_len, words], index=None, columns=None
    ).T

    return df


def save_file(df):

    if len(df) > 0:  # 데이터프레임에 데이터가 있을 경우에만 실행

        # CSV에서 이어쓰기 (mode="a")
        df.to_csv(
            # csv 파일 읽어오고
            path_or_buf="C:/AICC_STUDY/Project_test_01/data/IDKeywordData.csv",
            # 한글이 가능하게 인코딩
            encoding="cp949",
            # 이어쓰기 형식으로
            mode="a",
            # 인덱스 제거하고
            index=False,
            # 컬럼 없이
            columns=None,
            # 헤더 없이
            header=False,
        )
    else:
        pass


# +
# 크롤링하고 위에서 작성한 함수를 취합해서 실행하고 출력하는 함수
def getKeywordFile(id_list, name_list):
    # 변수 2개 사용을 위해 zip()으로 묶고 리스트화해서 슬라이싱 (필요할 경우 수정)
    for idn, name in list(zip(id_list, name_list))[:51]:

        # 키워드 별로 담기 위해 리스트 초기화
        titleList = []

        # 검색을 위해 name의 양식 수정
        search_name = name.replace(" ", "+")

        # 페이지 수 지정하여 for문 실행
        for i in range(1, 11, 1):
            # 주소 검색
            url = f"https://search.daum.net/search?w=news&nil_search=btn&DA=PGD&enc=utf8&cluster=y&cluster_page=1&q={search_name}&p={i}"
            print(url)
            response = requests.get(url)  # url 갖고오기
            html = response.text  # text만 갖고오기
            soup = BeautifulSoup(html, "html.parser")  # 파싱하기

            titles = soup.select(
                "ul.c-list-basic"
            )  # c-list-basic 클래스에서 ul에 묶여있는 요소들을 모두 갖고온다
            # subtitles = soup.select("a.elss.sub_tit")
            for title in titles:  # titles에서 title   # 갖고온 요소로 for문 실행
                titleText = title.text  # title.text만 추출
                titleList.append(titleText)  # titleList에 추가

            time.sleep(1)

        # 각 항목에 해당하는 키워드를 리스트로 받아서
        keywordData = trans_keywordList(get_keyword(titleList))

        # IDKeywordData.csv에 ID , Name , Keyword 형태로 저장
        save_file(rebornDataFrame(idn, name, keywordData))


# -
