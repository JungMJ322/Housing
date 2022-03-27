import csv
import json
from pyspark.sql import SparkSession
import save_mysql

spark = SparkSession.builder.master('local[1]').appName('hosp_change').getOrCreate()

def hospital_change():
    data = spark.read.json("/Housing/data/hadoop_upload/hospital.json", encoding='utf-8')
    data.createOrReplaceTempView('hospital')
    sql = 'select * from hospital where wgs84Lat is not NULL'
    data2 = spark.sql(sql)

    data_coll = data2.collect()
    rdr = list()
    for i in data_coll:
        rdr.append(i.asDict())
    temp_list = []
    count = 0
    for i in rdr:
        temp_dict = {}
        temp_dict['id'] = count
        temp_dict['place'] = i['dutyAddr']
        temp_dict['duty_code'] = i['dutyDiv']
        temp_dict['duty_Emcls_code'] = i['dutyEmcls']
        temp_dict['dutyEryn_code'] = i['dutyEryn']
        temp_dict['hname'] = i['dutyName']
        temp_dict['lat'] = i['wgs84Lat']
        temp_dict['lot'] = i['wgs84Lon']
        temp_list.append(temp_dict)
        count += 1

    # savefile("hospital", temp_list)
    save_mysql.save_list_to_db(temp_list, "hospital")
    df_data = spark.createDataFrame(temp_list)
    df_data.repartition(1).write.format('json').json("/Housing/data/output_json/hospital.json")
    

def savefile(filename, data):
    with open("../output_json/"+filename+".json", 'w', encoding='utf-8') as f:
        temp_dict = {data}
        f.write(json.dumps(temp_dict, ensure_ascii=False))

if __name__ == "__main__":
    hospital_change()