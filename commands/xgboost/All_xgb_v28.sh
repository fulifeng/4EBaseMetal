#!/bin/bash
cd ../../
python code/train_data_xgboost.py -gt All -d 2017-06-30 -s 1 -l 1 -c exp/3d/Co/logistic_regression/v3/LMCADY_v3.conf -v v28 -o tune > result/validation/xgboost/All_xgboost_l1_h1_v28.txt 2>&1 &

python code/train_data_xgboost.py -gt All -d 2017-06-30 -s 3 -l 1 -c exp/3d/Co/logistic_regression/v3/LMCADY_v3.conf -v v28 -o tune > result/validation/xgboost/All_xgboost_l1_h3_v28.txt 2>&1 &

python code/train_data_xgboost.py -gt All -d 2017-06-30 -s 5 -l 1 -c exp/3d/Co/logistic_regression/v3/LMCADY_v3.conf -v v28 -o tune > result/validation/xgboost/All_xgboost_l1_h5_v28.txt 2>&1 &

python code/train_data_xgboost.py -gt All -d 2017-06-30 -s 10 -l 1 -c exp/3d/Co/logistic_regression/v3/LMCADY_v3.conf -v v28 -o tune > result/validation/xgboost/All_xgboost_l1_h10_v28.txt 2>&1 &

python code/train_data_xgboost.py -gt All -d 2017-06-30 -s 20 -l 1 -c exp/3d/Co/logistic_regression/v3/LMCADY_v3.conf -v v28 -o tune > result/validation/xgboost/All_xgboost_l1_h20_v28.txt 2>&1 &

python code/train_data_xgboost.py -gt All -d 2017-06-30 -s 60 -l 1 -c exp/3d/Co/logistic_regression/v3/LMCADY_v3.conf -v v28 -o tune > result/validation/xgboost/All_xgboost_l1_h60_v28.txt 2>&1 &
cd commands/xgboost