hdfs dfs -mkdir /Housing
sleep(5)
hdfs dfs -mkdir /Housing/data
sleep(5)

spark-submit /Home/wovlf139/Housing/module/data_collection/data_collection.py
sleep(5)

hdfs dfs -put /Home/wovlf139/Housing/data/hadoop_upload /Housing/data
sleep(5)

spark-submit /Home/wovlf139/Housing/module/data_process/data_process.py
sleep(5)