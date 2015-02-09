import numpy as np
import os
import re
import pylab as pl
import sys
import getopt
import pdb
from random import shuffle
from os.path import isfile

def strType(var):
    try:
        if int(var) == float(var):
            return 'int'
    except:
        try:
            float(var)
            return 'float'
        except:
            return 'str'

def runExp(fname_command, varargin,fname_prefix=[]):
    pdb.set_trace()

    if len(fname_prefix) ==0:
        fname_prefix = '../Results/'+fname_command
        fname_command = fname_command + '('

    if len(varargin)>1:
        valname = varargin[0].replace(' ','').replace(',','')
        vallist = varargin[1].replace(' ','').replace('"','').split(',')
        varargin = varargin[2:]

    #for val in shuffle(valist)
    shuffle(vallist)
    for val in vallist:
        fname_prefix2 = fname_prefix+'_'+valname+'_'+val
        fname_command2 = fname_command+'_'+val

        if len(varargin) == 0:
            log_fname_started = fname_prefix2+'.started'
            log_fname_finished = fname_prefix2+'.finished'
            if isfile(log_fname_started) or isfile(log_fname_finished):
                print 'file '+fname_prefix2+' exists... skip!'
                continue
            strat_log_id = open(log_fname_started,'w')

            # run experiment
            str_cmd = fname_command2+')'
            print 'Running '+ str_cmd

            # evoke function
            os.remove(log_fname_started)
            finish_log_id = open(log_fname_finished,'w')

        elif len(varargin) == 1:
            sys.exit('length of varargin should be even number!')
        else:
            batch_general(fname_command2+',', fname_prefix2,varargin)



try:
    opts, args=getopt.getopt(sys.argv[1:], "hm:p:",
            ["module_name=","parameters="])
except getopt.GetoptError:
    print 'gae_demo.py -i <inputfile>'
    sys.exit(2)

for opt, arg in opts:
    if opt =='-h':
    	exit()
    elif opt in("-m","--module_name="):
	module_name = arg
    elif opt in("-p","--parameters="):
	parameters = arg

varargin_tokens = re.split(r'[\[\]]',parameters)[:-1]

runExp(module_name, varargin_tokens,[])

'''    
    result_dir = '../Results/'
    if not os.isdir(result_dir):
        os.makedirs(result_dir)
    result = [hyp1,hyp2,hyp3]
    return result
    np.savetxt(result_dir+'hyp1_'+str(hyp1)+'_hyp2_'+str(hyp2)+'_hyp3_'+str(hyp3)+'_.csv',[hyp1,hyp2,hyp3],delimiter=',')
'''

