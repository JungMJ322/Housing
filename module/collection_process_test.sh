#!/usr/bin/env bash

HERE=$(dirname $(realpath $0))
echo HERE

hdfs dfs -mkdir /Housing
sleep 5

hdfs dfs -mkdir /Housing/data
sleep 5

spark-submit data_collection/data_collection.py
sleep 5

hdfs dfs -put ../../data/hadoop_upload /Housing/data
sleep 5

spark-submit ../data_process/data_process.py
sleep 5

exit 0