import csv
import json
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

spark = SparkSession.builder.master('local[1]').appName('sold_cost').getOrCreate()


def create_code_dict():
    with open('../../data/hadoop_upload/sold_cost/area_code.txt', 'r', encoding='euc-kr') as f:
        rdr = csv.reader(f, delimiter='\t')
        code_dict = {}

        for row in rdr:
            code_dict[row[1]] = row[0]

        return code_dict


def save_json():
    temp_list = []
    code_dict = create_code_dict()
    # for i in range(1, 13):
    #     data = spark.read.csv("/Housing/data/hadoop_upload/sold_cost/21."+str(i)+".csv", encoding="cp949", header=True)
    #     data_coll = data.collect()
    #     rdr = list()
    #
    #     for j in data_coll:
    #         rdr.append(j.asDict())
    #
    #     for j in rdr:
    #         temp = dict()
    #         temp['place'] = j["시군구"]
    #         temp['area_grade'] = str(int(float(j["전용면적(㎡)"]) // 10)) + '단위'
    #         try:
    #             temp['place_code'] = code_dict[j["시군구"]]
    #         except KeyError:
    #             continue
    #         temp['month'] = j["계약년월"]
    #         temp['cost'] = int(j["거래금액(만원)"].replace(",", ""))
    #         temp_list.append(temp)
    #
    # for i in range(1, 13):
    #     data = spark.read.csv("/Housing/data/hadoop_upload/sold_cost/20."+str(i)+".csv", encoding="cp949", header=True)
    #     data_coll = data.collect()
    #     rdr = list()
    #
    #     for j in data_coll:
    #         rdr.append(j.asDict())
    #
    #     for j in rdr:
    #         temp = dict()
    #         temp['place'] = j["시군구"]
    #         temp['area_grade'] = str(int(float(j["전용면적(㎡)"]) // 10)) + '단위'
    #         try:
    #             temp['place_code'] = code_dict[j["시군구"]]
    #         except KeyError:
    #             continue
    #         temp['month'] = j["계약년월"]
    #         temp['cost'] = int(j["거래금액(만원)"].replace(",", ""))
    #         temp_list.append(temp)

    for i in range(1, 3):
        data = spark.read.csv("/Housing/data/hadoop_upload/sold_cost/22." + str(i) + ".csv", encoding="cp949", header=True)
        data_coll = data.collect()
        rdr = list()

        for j in data_coll:
            rdr.append(j.asDict())

        for j in rdr:
            temp = dict()
            temp['place'] = j["시군구"]
            temp['area_grade'] = str(int(float(j["전용면적(㎡)"]) // 10)) + '단위'
            try:
                temp['place_code'] = code_dict[j["시군구"]]
            except KeyError:
                continue
            temp['month'] = j["계약년월"]
            temp['cost'] = int(j["거래금액(만원)"].replace(",", ""))
            temp_list.append(temp)

    df_data = spark.createDataFrame(temp_list)
    df_data.createOrReplaceTempView("df_data")
    data_for_save = df_data.groupBy('area_code', 'area_grade', 'month').agg(F.avg(F.col('cost')).alias('mean_cost'))
    user = "root"
    password = "1234"
    url = "jdbc:mysql://localhost:3306/Housing"
    driver = "com.mysql.cj.jdbc.Driver"
    dbtable = "sold_cost_mean"
    data_for_save.write.jdbc(url, dbtable, "append", properties={"driver": driver, "user": user, "password": password})


if __name__ == "__main__":
    save_json()