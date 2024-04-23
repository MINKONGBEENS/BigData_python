import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd

ServiceKey = "%2BwH3doM%2FWWlSWEmYMT2LJh%2BxKmnDTTIxJhQj9QDU6La4M77N2xZqyN%2Bs19D%2BiOQpGtU7iUBb0%2F7Sgld0OA6V%2Fg%3D%3D"

def main():
    result = [] # 결과를 리스트 형태로 받음
    natName='' 
    print("==== 국내 입국한 외국인의 통계 데이터를 수집합니다. ====")
    nat_cd = input('국가 코드를 입력하세요(중국: 112 / 일본: 130 / 미국: 275) : ')
    nStartYear =int(input('데이터를 몇 년부터 수집할까요? : '))
    nEndYear = int(input('데이터를 몇 년까지 수집할까요? : '))
    
    ed_cd = "E" # 방한외래관광객 : E , 해외출국 : D
    
    result, natName, ed, dataEND = getTourismStatsService(nat_cd,ed_cd, nStartYear, nEndYear)
    # 첫 번째 함수 호출
    # result, natName, ed, dataEnD에 각각 getTourismStatsService()함수를 호출하여 요소를 부여함
    # 입력받은 nat_cd, nStartYear, nEndYear, ed_cd를 인자로 부여해 함수를 호출하고,
    # 그 반환 값을 각각 result, natName, ed, dataEND에 할당함
    
    
    # 위 구문에서 함수를 호출하고 natName 변수에 값을 할당해주었는데,
    # 잘못된 접근이라면 값이 할당되지 않고 초기값인 공백이 남게되므로,
    # if(natName == '') 의 형태로 데이터 제공의 유무를 판단하여
    # 예외처리를 할지, 혹은 추가적인 작업을 실행시킬지를 결정할 수 있다.
    
    if (natName=='') : # URL 요청은 성공하였지만, 데이터 제공이 안된 경우
        print('데이터가 전달되지 않았습니다. 공공데이터포털의 서비스 상태를 확인하기 바랍니다.')
        
    else: # URL 요청에 성공했고, 데이터 제공도 정상적으로 받았을 경우, 받아온 데이터를 전처리하여 csv 파일로 저장하는 구문
        columns = ["입국자국가", "국가코드", "입국연월", "입국자 수"]
        result_df = pd.DataFrame(result, columns = columns)
        result_df.to_csv('./%s_%s_%d_%s.csv' % (natName, ed, nStartYear, dataEND),index=False, encoding='cp949')    


def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear) :
    
    # GPT 수정 : 함수의 매개변수 ed를 초기화했습니다.

    result = []
    natName=''
    ed = ''  # GPT 수정 : ed 변수를 초기화
  
    dataEND = "{0}{1:0>2}".format(str(nEndYear), str(12))
    
    isDataEnd = 0 # 데이터 끝 확인용 flag 초기화
    
    for year in range(nStartYear, nEndYear+1):
        for month in range(1, 13): # 각 연도별로 1 ~ 12월까지 월을 생성해주는 단계
            if(isDataEnd == 1): 
                break # isDataEnd가 1이면, 데이터가 더 이상 없다는 flag 이므로 for문 중지
              
            yyyymm = "{0}{1:0>2}".format(str(year), str(month))
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd) # 3번째 함수 호출
          
            if (jsonData['response']['header']['resultMsg'] == 'OK'):
                if jsonData['response']['body']['items'] == '':
                    dataEND = "{0}{1:0>2}".format(str(year), str(month-1))
                    print("데이터 없음.... \n 제공되는 통계 데이터는 %s년 %s월까지입니다."
                          %(str(year), str(month-1)))
                    isDataEnd = 1 # 데이터 종료 flag 설정
                    break
                
                print (json.dumps(jsonData,indent=4, sort_keys=True, ensure_ascii=False))
                natName = jsonData['response']['body']['items']['item']['natKorNm'] 
                natName = natName.replace(' ', '') # 공백 및 데이터가 없는 내용 삭제
                num = jsonData['response']['body']['items']['item']['num']
                ed = jsonData['response']['body']['items']['item'].get('ed', '')  # ed 정보가 없는 경우 공백으로 처리 (GPT로 수정)
                print('[ %s_%s : %s ]' % (natName, yyyymm, num))
                print('----------------------------------------------------------------------')
                result.append([natName, nat_cd, yyyymm, num])
                  
    return result, natName, ed, dataEND



def getTourismStatsItem(yyyymm, national_code, ed_cd):
    
    # GPT 수정 : 함수의 설명을 추가했습니다.
   
  
    service_url = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList"
    parameters = "?_type=json&serviceKey=" + ServiceKey   # 인증키
    parameters += "&YM=" + yyyymm
    parameters += "&NAT_CD=" + national_code
    parameters += "&ED_CD=" + ed_cd
    url = service_url + parameters
    
    # 받는 사람 : service_url
    # parameter : 보내는 사람 , 요청을 목록형으로 추가하여 보냄
    # 목록형 : dict 자료형처럼 Key : Value 로

    retData = getRequestUrl(url) # 4번째 함수 호출
    
    if (retData == None):
        return None
    else:
         return json.loads(retData)



# getRequestUrl() 함수를 이용해 원하는 검색 조건에 맞는 데이터를 요청하고,
# 이에 대한 응답을 getRequestUrl()을 호출한 getTourismStatsItem()의 retData에 반환함

def getRequestUrl(url):
    
    # GPT 수정 : 함수의 설명을 추가했습니다.
    
    req = urllib.request.Request(url) # request 메시지 생성
    
    
    
    try:
        response = urllib.request.urlopen(req)# req를 서버에 전달하고 내용을 받아 response에 저장
        
        if response.getcode() == 200: # 반환 받은 결과코드가 정상코드(200)일 경우
            print ("[%s] Url Request Success" % datetime.datetime.now())
            # 사용자에게 성공적으로 실행됐음을 알리고,
            return response.read().decode('utf-8')
            # 데이터를 한글로 인코딩 하고, return값으로 실어 getRequestUrl()을 호출한 getTourismStatsItem()의 retData에 저장
          
          
          
    except Exception as e: # 결과코드가 정상코드가 아닐 경우의 예외처리
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None
        # 사용자에게 에러가 있음을 알리고, 아무것도 반환하지 않음




# 파이썬에는 main() 함수부터 시작하라는 규칙이 없음
# 가장 먼저 등장하는 함수가 가장 먼저 실행되므로, 아래 구문을 통해
# main() 함수가 가장 먼저 실행 되도록 호출해준다.
if __name__ == '__main__':
    main()




#------------------------------------------------------------------------------------------------------------
# GPT 구문 요약
#------------------------------------------------------------------------------------------------------------

# 이 코드는 국내 입국한 외국인의 통계 데이터를 수집하고 처리하는 기능을 수행합니다. 코드의 전체적인 동작 원리와 효과는 다음과 같습니다

# 1. 사용자 입력 : 프로그램이 실행되면 사용자로부터 국가 코드, 데이터 수집 기간 등의 입력을 받습니다.
# 2. 데이터 수집 요청 : 사용자가 입력한 정보를 기반으로 해당 국가의 통계 데이터를 공공데이터포털에서 요청합니다.
# 3. 데이터 수집 : 요청한 데이터는 `getTourismStatsItem()` 함수에서 처리됩니다. 이 함수는 인자로 전달된 연도와 국가 코드 등을 기반으로 데이터를 요청하고, 응답을 받아옵니다.
# 4. 데이터 처리 : 받아온 데이터는 JSON 형식으로 제공됩니다. 이 데이터를 `getTourismStatsService()` 함수에서 처리하고 필요한 정보를 추출합니다.
# 5. 결과 반환 : 처리된 결과는 적절한 형태로 정리된 후, `main()` 함수로 반환됩니다. 이 결과에는 국가명, 국가 코드, 입국 연월, 입국자 수 등의 정보가 포함됩니다.
# 6. 결과 출력 또는 저장 : `main()` 함수에서는 처리된 결과를 화면에 출력하거나 CSV 파일로 저장합니다.

#------------------------------------------------------------------------------------------------------------

# 함수의 호출과 반환 과정은 다음과 같습니다

# main() 함수가 가장 먼저 실행됩니다.
# main() 함수 내에서는 getTourismStatsService() 함수를 호출하여 데이터를 수집하고 처리합니다.
# getTourismStatsService() 함수는 데이터 수집 기간 동안 반복적으로 `getTourismStatsItem()` 함수를 호출하여 데이터를 받아옵니다.
# getTourismStatsItem() 함수는 요청된 데이터를 받아와서 처리한 후, 처리된 결과를 반환합니다.

#------------------------------------------------------------------------------------------------------------




#------------------------------------------------------------------------------------------------------------
# 각 함수별 기능 상세 설명
#------------------------------------------------------------------------------------------------------------

# main() 함수

# 기능 : 프로그램의 주요 제어를 담당합니다. 사용자로부터 국가 코드, 데이터 수집 기간 등을 입력받고, 데이터 수집 및 처리를 호출하여 수행합니다.

# 동작 원리

# 사용자로부터 국가 코드, 데이터 수집 기간을 입력 받습니다.
# 입력된 정보를 기반으로 getTourismStatsService() 함수를 호출하여 데이터 수집 및 처리를 수행합니다.
# 수집된 데이터를 화면에 출력하거나 CSV 파일로 저장합니다.

#------------------------------------------------------------------------------------------------------------

# getTourismStatsService() 함수:

# 기능 : 국가별 입국 외국인 통계 데이터를 수집하고 처리합니다.

# 동작 원리

# 입력된 국가 코드, 데이터 수집 기간을 기반으로 해당 기간 동안의 데이터를 수집합니다.
# getTourismStatsItem() 함수를 반복 호출하여 각 연도 및 월에 해당하는 데이터를 수집합니다.
# 수집된 데이터를 처리하여 필요한 정보를 추출하고 결과를 반환합니다.

#------------------------------------------------------------------------------------------------------------

# getTourismStatsItem() 함수:

# 기능 : 특정 연도 및 월에 해당하는 국가별 입국 외국인 통계 데이터를 요청하고 처리합니다.

# 동작 원리

# 입력된 연도, 월, 국가 코드 등의 정보를 기반으로 특정 기간의 통계 데이터를 요청합니다.
# 공공데이터포털에서 받은 응답을 처리하여 필요한 정보를 추출합니다.
# 추출된 정보는 getTourismStatsService() 함수로 반환됩니다.

#------------------------------------------------------------------------------------------------------------