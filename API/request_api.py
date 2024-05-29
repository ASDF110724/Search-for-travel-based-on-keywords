import requests
from func_def import make_url
import urllib3

urllib3.disable_warnings()


url = "http://apis.data.go.kr/B551011/KorService1/API&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=AppTest&areaCode=1&_type=json"
# 요청에 필요한 파라미터를 설정합니다.

url2 = "http://apis.data.go.kr/B551011/KorService1/areaCode1"

params = {
    # YOUR API KEY
    "serviceKey": "APIKey",  # 발급받은 API 키
    "_type": "json",  # 반환 타입 (json, xml)
    "numOfRows": "10",  # 한 페이지 결과 수
    "pageNo": "1",  # 페이지 번호
    "MobileApp": "AppTest",  # 시/도 이름
    "MobileOS": "ETC",  # 버전
    "areaCode": "1",  # 지역코드
}

print(make_url(url2, params))


# GET 요청을 보냅니다.
# response = requests.get(url, verify=False)

# data = response.text
# print(data)
