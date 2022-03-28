#!/usr/bin/env bash

HERE=$(dirname $(realpath $0))
echo HERE

hdfs dfs -mkdir /Housing
sleep 5

hdfs dfs -mkdir /Housing/data
sleep 5

# spark-submit cu.py
# sleep 5

spark-submit detailed_inquiry.py
sleep 5

spark-submit competition_rate.py
sleep 5

spark-submit getHospital.py
sleep 5

# spark-submit GS25.py
# sleep 5

spark-submit sevenEleven.py
sleep 5

spark-submit xlsxToJson.py
sleep 5

hdfs dfs -put ../../data/hadoop_upload /Housing/data
sleep 5

spark-submit ../data_process/data_process.py
sleep 5

exit 0