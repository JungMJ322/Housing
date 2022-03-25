import json
from convinient_change import savefile
from pyspark.sql import SparkSession

spark = SparkSession.builder.master('local[1]').appName('compet').getOrCreate()

def compet_change():
    data = spark.read.json("/Housing/data/hadoop_upload/competitionData0.json")
    data_coll = data.collect()
    rdr = list()
    for i in data_coll:
        rdr.append(i.asDict())

    total_list = []
    for i in rdr:
        temp_dict = {}
        temp_dict["HOUSE_MANAGE_NO"] = i["HOUSE_MANAGE_NO"]
        temp_dict["AREA_GRADE"] = i['area_grade']
        temp_dict["TOTAL_REQ"] = i["REQ_CNT"]
        temp_dict["COMPET_RATE"] = i["CMPET_RATE"]
        temp_dict["AVR_SCORE"] = i["AVRG_SCORE"]
        temp_dict["BOTTOM_SCORE"] = i["LWET_SCORE"]
        temp_dict["TOP_SCORE"] = i["TOP_SCORE"]
        temp_dict["MODEL_NO"] = i["MODEL_NO"]
        total_list.append(temp_dict)
    total_list_changed = list(map(dict, set(tuple(sorted(d.items())) for d in total_list)))

    savefile(" ", "competition", total_list_changed)


if __name__ == "__main__":
    compet_change()
