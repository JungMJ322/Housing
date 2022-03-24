from pymongo import MongoClient, GEOSPHERE
from bson import SON
import pandas as pd
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.master('local[1]').appName('getInfra').getOrCreate()

client = MongoClient('localhost', 27017)
db = client['test']

infra_json_list = ['school', 'subway2', 'park', 'mart', 'busStop']

def makeMongoSet(infra=infra_json_list[0]):

    infra_file = spark.read.json(f'/housing/data/{infra}.json')

    infra_lat = infra_file.select('lat').rdd.flatMap(lambda x: x).collect()
    infra_lot = infra_file.select('lot').rdd.flatMap(lambda x: x).collect()
    infra_id = infra_file.select('school_id').rdd.flatMap(lambda x: x).collect()

    geo_list = list()
    for i in range(len(infra_lat)):
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
    detail = spark.read.format('json').option("multiline", "true").json(f'/housing/data/detail.json')
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
        
        row_list = list()
        for doc in infra_loca:
            row_list.append(doc['id'])
        
        info_list.append(row_list)

    return info_list

if __name__ == '__main__':
    detail = detailData()

    makeMongoSet()

    loca = getInfraLoca(detail)

    df = pd.DataFrame({
        'HOUSE_MANAGE_NO': detail['id'],
        'school': loca
    })

    print(df)