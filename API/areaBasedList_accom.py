# 코드 목적: 지역기반 관광정보조회 (숙박(32) 관광정보 전체조회)
# 작성자: 최한영
# 작성일: 2024-05-20
# 상세 설명: 투어 API의 지역코드와 관광코드를 조합하여 여행지 정보 조회

import requests
from func_def import *

url = "http://apis.data.go.kr/B551011/KorService1/areaBasedList1"


### INPUT ###

# 관광타입
contentTypeId = "32"

# 지역코드
areaCode = "1"

# 시군구코드
sigunguCode = "1"

##############

params = {
    # 필수
    "numOfRows": "10",
    "pageNo": "1",
    "MobileOS": "ETC",
    "MobileApp": "AppTest",
    # YOUR API KEY
    "serviceKey": "APIKey",
    # 선택
    "_type": "json",
    "listYN": "Y",
    "arrange": "A",
    "contentTypeId": contentTypeId,  # 관광타입
    "areaCode": areaCode,  # 지역코드
    "sigunguCode": sigunguCode,  # 시군구코드
    #    'cat1':'B02',                       # 대분류
    #    'cat2':'B0201',                     # 중분류
    #    'cat3':'B02010100',                 # 소분류
    #    'modifiedtime':'20240721'           # 수정일
}

response = requests.get(make_url(url, params), verify=False)

if response.status_code == 200:
    print(response.text)
    make_csv(response.text, "지역기반 숙박(32)정보 조회", "areaBasedList_accom")
else:
    print(f"Error: {response.status_code}")
