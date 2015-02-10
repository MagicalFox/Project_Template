import numpy as np
import pylab as pl
import pdb
import csv
import sys

def main(parameters):
    try:
        hyp1 = parameters[0]
        hyp2 = parameters[1]
    except:
        sys.exit('Number of passed in arguments does not match with the function main.')
    result_dir = '../Results/'
    result_file_name = result_dir + 'Exp_hyp1_'+str(hyp1)+'_hyp2_'+str(hyp2)+'_.csv'
    # Actuall code goes in here
    pl.pause(5)
    print 'In tempCode.main: '+ result_file_name 
