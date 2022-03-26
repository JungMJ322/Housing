#!/usr/bin/env bash

export HERE=$(dirname $(realpath $0))

hdfs dfs -mkdir /Housing
sleep 5

hdfs dfs -mkdir /Housing/data
sleep 5

spark-submit HERE/data_collection/data_collection.py
sleep 5

hdfs dfs -put HERE/../data/hadoop_upload /Housing/data
sleep 5

spark-submit HERE/data_process/data_process.py
sleep 5

exit 0