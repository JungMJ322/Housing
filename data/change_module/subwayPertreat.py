import pandas as pd
import json
import getLocation
from pyspark.sql import SparkSession

spark = SparkSession.builder.master('local[1]').appName('getInfra').getOrCreate()

location = '../data/json/'
file_name = 'subway.json'
json_name = 'subway2.json'

def subwayPer(location=location, file_name=file_name, json_name=json_name):

    df_json = spark.read.json(f'/Housing/data/hadoop_upload/{file_name}')
    df_json.createOrReplaceTempView('subway')
    df_json2 = spark.sql("""select 역번호 as subway_code, 역사명 as stn_name, 노선명 as route_name, 
                            역위도 as lat, 역경도 as lot 역사 도로명주소 as place form subway""")
    
    df_json3 = df_json2.collect()

    json_file = list()
    for doc in df_json3:
        json_file.append(doc.asDict())

    cnt = 0
    for data in json_file:
        if data['lot'] == None:
            loca_dict = getLocation.kakao_location(data['place'])
            data['lot'] = loca_dict['lot']
            data['lat'] = loca_dict['lat']
        data['id'] = cnt
        cnt = cnt + 1

    with open((location + file_name), 'w', encoding='utf8') as f:
        json.dump(json_file['data'], f, ensure_ascii=False)

if __name__ == '__main__':
    subwayPer()
