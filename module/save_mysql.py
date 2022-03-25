from pyspark.sql import SparkSession
import json
spark = SparkSession.builder.master('local[1]').appName('jsonToMysql').getOrCreate()


def save_mysql(filename, table_name):
    rdr = spark.read.format('json').option("multiline", "true").json(f'/housing/data/json/{filename}')
    user = "root"
    password = "1234"
    url="jdbc:mysql://localhost:3306/Housing"
    driver = "com.mysql.cj.jdbc.Driver"
    dbtable = table_name
    df_spark = spark.createDataFrame(rdr)
    df_spark.write.jdbc(url, dbtable, "append", properties={"driver": driver, "user": user, "password": password})

if __name__ == '__main__':
    save_mysql('park.json', 'park')