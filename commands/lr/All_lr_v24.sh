#!/bin/bash
cd ../../
python code/train_data_lr.py -gt all -d 2017-06-30 -s 1 -l 1 -c exp/3d/Co/logistic_regression/v3/LMCADY_v3.conf -v v24 -o tune > /dev/null 2>&1 &
python code/train_data_lr.py -gt all -d 2017-06-30 -s 3 -l 1 -c exp/3d/Co/logistic_regression/v3/LMCADY_v3.conf -v v24 -o tune > /dev/null 2>&1 &
python code/train_data_lr.py -gt all -d 2017-06-30 -s 5 -l 1 -c exp/3d/Co/logistic_regression/v3/LMCADY_v3.conf -v v24 -o tune > /dev/null 2>&1 &
python code/train_data_lr.py -gt all -d 2017-06-30 -s 10 -l 1 -c exp/3d/Co/logistic_regression/v3/LMCADY_v3.conf -v v24 -o tune > /dev/null 2>&1 &
python code/train_data_lr.py -gt all -d 2017-06-30 -s 20 -l 1 -c exp/3d/Co/logistic_regression/v3/LMCADY_v3.conf -v v24 -o tune > /dev/null 2>&1 &
python code/train_data_lr.py -gt all -d 2017-06-30 -s 60 -l 1 -c exp/3d/Co/logistic_regression/v3/LMCADY_v3.conf -v v24 -o tune > /dev/null 2>&1 &
cd commands/lr