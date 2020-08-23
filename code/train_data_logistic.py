import os
import sys
import argparse
from copy import copy
sys.path.insert(0,os.path.abspath(os.path.join(sys.path[0],"..")))
from live.Logistic_live import Logistic_online

if __name__ == '__main__':
    desc = 'the logistic regression model'
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
    parser.add_argument('-C', '--C', type=float)
    args = parser.parse_args()
    model = Logistic_online(lag = args.lag, horizon = args.steps, version = args.version, gt = args.ground_truth, date = args.date, source = args.source)
    if args.action=="tune":
        model.tune(100)
    elif args.action=='train':
        model.train(C=args.C, max_iter=args.max_iter)
    else:
        final = model.test()
