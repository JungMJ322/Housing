from pymongo import MongoClient, GEOSPHERE
from bson import SON
import pandas as pd
import pyspark
from pyspark.sql import SparkSession
import json

spark = SparkSession.builder.master('local[1]').appName('getInfra').getOrCreate()

client = MongoClient('localhost', 27017)
db = client['test']

infra_json_list = ['hospital'] #'school', 'subway', 'mart', 'park', 

user = 'root'
password = '1234'
url = 'jdbc:mysql://localhost:3306/Housing'
driver = 'com.mysql.cj.jdbc.Driver'
dbtable='infra'

def makeMongoSet(infra=infra_json_list[0]):

    infra_file = spark.read.json(f'/Housing/data/output_json/{infra}.json')
    infra_file.createOrReplaceTempView(infra)

    sql = f'select id, lat, lot from {infra} where lat is not NULL or lat != ""'
    infra_file2 = spark.sql(sql)
    
    infra_lat = infra_file2.select('lat').rdd.flatMap(lambda x: x).collect()
    infra_lot = infra_file2.select('lot').rdd.flatMap(lambda x: x).collect()
    infra_id = infra_file2.select('id').rdd.flatMap(lambda x: x).collect()

    geo_list = list()
    for i in range(len(infra_id)):
        geo_dict = dict()
        geo_dict['id'] = infra_id[i]
        coordinates = [float(infra_lot[i]), float(infra_lat[i])]
        geo_dict['location'] = {'type': 'Point', 'coordinates': coordinates}
        geo_list.append(geo_dict)

    infra_mongo = db[infra]
    infra_mongo.drop()
    infra_mongo = db[infra]

    infra_mongo.insert_many(geo_list)
    


def detailData():
    detail = spark.read.format('json').option("multiline", "true").json(f'/Housing/data/output_json/detail.json')
    detail.createOrReplaceTempView('detail')

    sql = 'select HOUSE_MANAGE_NO, lat, lot from detail where lat is not NULL'
    detail2 = spark.sql(sql)

    housing_id = detail2.select('HOUSE_MANAGE_NO').rdd.flatMap(lambda x: x).collect()
    housing_lot = detail2.select('lot').rdd.flatMap(lambda x: x).collect()
    housing_lat = detail2.select('lat').rdd.flatMap(lambda x: x).collect()

    housing = dict()
    housing['id'] = housing_id
    housing['lot'] = housing_lot
    housing['lat'] = housing_lat

    return housing


def getInfraLoca(detail, infra=infra_json_list[0]):
    infra_mongo = db[infra]
    
    # query = {'location': {'$near': SON([('$geometry', SON([('type', 'Point'), ('coordinates', [float(detail['lot'][i]), float(detail['lat'][i])])])), ('$maxDistance', 1000)])}}

    infra_mongo.create_index([("location", GEOSPHERE)])

    info_list = list()
    for i in range(len(detail['id'])):
        infra_loca = infra_mongo.find({'location': {'$near': SON([('$geometry', SON([('type', 'Point'), ('coordinates', [float(detail['lot'][i]), float(detail['lat'][i])])])), ('$maxDistance', 1000)])}})
        
        row_dict = dict()
        row_list = list()
        for doc in infra_loca:
            row_list.append(doc['id'])

        row_dict['id'] = row_list
        info_list.append(json.dumps(row_dict))

    return info_list

def save_data():
    detail = detailData()

    # makeMongoSet(infra_json_list[0])
    # loca = getInfraLoca(detail, infra_json_list[0])

    loca = list()
    for data in infra_json_list:
        makeMongoSet(data)
        row = getInfraLoca(detail, data)

        
        loca.append(row)

    # df = pd.DataFrame({
    #     'HOUSE_MANAGE_NO': detail['id'],
    #     'infra': loca
    # })

    df = pd.DataFrame({
        'HOUSE_MANAGE_NO': detail['id'],
        infra_json_list[0]: loca[0],
        'subway': loca[1],
        infra_json_list[2] : loca[2],
        infra_json_list[3] : loca[3]
    })

    print(df)

    df_spark = spark.createDataFrame(df)
    df_spark.write.jdbc(url, dbtable, "overwrite", properties={"driver":driver, "user":user, "password":password})


    if __name__ == '__main__':
        save_data()