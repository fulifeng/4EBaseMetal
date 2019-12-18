import os
import sys
import json
import argparse
import numpy as np
import pandas as pd
from copy import copy
sys.path.insert(0, os.path.abspath(os.path.join(sys.path[0], '..')))
import warnings
from live.ALSTM_live import ALSTM_online

if __name__ == '__main__':
  desc = 'the XGBoost model'
  parser = argparse.ArgumentParser(description=desc)
  parser.add_argument('-c','--config',type=str,default="",
            help='configuration file path')
  parser.add_argument('-s','--steps',type=int,default=5,
            help='steps in the future to be predicted')
  parser.add_argument('-gt', '--ground_truth', help='ground truth column',
            type=str, default="LME_Co_Spot")
  parser.add_argument('-max_iter','--max_iter',type=int,default=100,
            help='max number of iterations')
  parser.add_argument(
      '-sou','--source', help='source of data', type = str, default = "NExT")
  parser.add_argument(
      '-l','--lag', type=int, default = 5, help='lag')
  parser.add_argument('-v','--version', help='version', type = str, default = 'v10')
  parser.add_argument('-o', '--action', type=str, default='train',
            help='train, test, tune')
  parser.add_argument('-d', '--date', help = "the date is the final data's date which you want to use for testing",type=str)	
  parser.add_argument('-log', '--log', type=str)
  parser.add_argument('-script', '--script', type=str)
  parser.add_argument(
      '-e', '--epoch', type=int, default=50,
      help='the number of epochs')
  parser.add_argument(
      '-b', '--batch', type=int, default=1024,
      help='the mini-batch size')
  parser.add_argument(
      '-i', '--interval', type=int, default=1,
      help='save models every interval epoch')
  parser.add_argument(
      '-lrate', '--lrate', type=float, default=0.001,
      help='learning rate')
  parser.add_argument(
      '-t', '--test', action='store_true',
      help='train or test')
  parser.add_argument(
      '-m', '--model', type=str, default='',
      help='the model name(after encoder/decoder)'
  )
  parser.add_argument(
      '-hidden','--hidden_state',type=int, default=50,
      help='number of hidden_state of encoder/decoder'
  )
  parser.add_argument(
      '-split', '--split', type=float, default=0.9,
      help='the split ratio of validation set')
  parser.add_argument(
      '-drop','--drop_out', type=float, default = 0.3,
      help='the dropout rate of LSTM network'
  )
  parser.add_argument(
      '-a','--attention_size', type = int, default = 2,
      help='the head number in MultiheadAttention Mechanism'
  )
  parser.add_argument(
      '-embed','--embedding_size', type=int, default = 5,
      help='the size of embedding layer'
  )
  parser.add_argument(
      '-lambd','--lambd',type=float,default = 0,
      help='the weight of classfication loss'
  )
  parser.add_argument(
      '-savep','--save_prediction',type=bool, default=0,
      help='whether to save prediction results'
  )
  parser.add_argument(
      '-savel','--save_loss',type=bool, default=0,
      help='whether to save loss results'
  )
  args = parser.parse_args()
  for date in for date in ["2014-12-31","2015-06-30","2015-12-31","2016-06-30","2016-12-31","2017-06-30","2017-12-31","2018-06-30","2018-12-31"]:
    model = ALSTM_online(lag = args.lag, horizon = args.steps, version = args.version, gt = args.ground_truth, date = date, source = args.source, path =args.config)
    if args.action=="tune":
      model.choose_parameter(log = args.log, script = args.script)
    elif args.action=='train':
      model.train(
          num_epochs=args.epoch,
  				batch_size=args.batch,
          split=args.split,
  				drop_out=args.drop_out,
  				hidden_state=args.hidden_state,
  				embedding_size=args.embedding_size,
  				lrate=args.lrate,
  				attention_size=args.attention_size,
  				interval=args.interval,
  				lambd=args.lambd,
  				save_loss=args.save_loss,
  				save_prediction=args.save_prediction)
    else:
      final = model.test(split = args.split)
      final.to_csv("_".join([args.ground_truth,args.date,str(args.steps),args.version])+".csv")
