# Usage:
# make sure that the Project Template folder structure is followed.  
# In terminal run:  python batch_general.py -m tempCode -p 'p1 [ BB, UCF101] p2 [3, 1]'
# Note:
# 1. -m flag model name, the model has to have the code in def main()
# 2. -p flag parameters which is passed in as one single string variable. each hyperparameter name is followed by a list of values in a pire of [], even if there is only one value, separated by space. The values in the lists are separated by ','.  
# 3. string variable values can be in pairs of '' or "" or none.
# 4. Log file use the naming convention that each token is separated by '_' so avoid naming variables using '_'
# 5. Parameters are stored in both the start and finish log file. If the parameter has large volume, use -s 0 flag to supress saving.
 
# Example: 
# python batch_general.py -m tempCode -p 'p1 [ BB, UCF101] p2 [3, 1]'
# Example 2:
# python batch_general.py -m tempCode -p 'p1 [ "BB", "UCF101"] p2 [3, 1]'
# The code support empty argument but the current version doesn't support Python's default value syntax




import numpy as np
import os
import re
import pylab as pl
import sys
import getopt
import pdb
import time
import random
from os.path import isfile

def convertType(var):
    try:
        return  int(var)
    except:
        try:
            return float(var)
        except:
            return var

def runExp(fname_command, varargin,fname_prefix=[],save = 1):

    if len(fname_prefix) ==0:
        Log_dir = '../Results/Log/'
        if not os.path.isdir(Log_dir):
            os.makedirs(Log_dir)
        fname_prefix = '../Results/Log/'+fname_command
        fname_command = fname_command + '('

    if len(varargin)>1:
        valname = varargin[0].replace(' ','').replace(',','')
        vallist = varargin[1].replace(' ','').replace('"','').split(',')
        varargin = varargin[2:]

    #for val in shuffle(valist)
    random.shuffle(vallist)
    for val in vallist:
        fname_prefix2 = fname_prefix+'_'+valname+'_'+val
        fname_command2 = fname_command+val

        if len(varargin) == 0:
            log_fname_started = fname_prefix2+'.started.npy'
            log_fname_finished = fname_prefix2+'.finished.npy'
            if isfile(log_fname_started) or isfile(log_fname_finished):
                print 'file '+fname_prefix2+' exists... skip!'
                continue
            strat_log_id = open(log_fname_started,'w')
            # run experiment
            str_cmd = fname_command2+')'
            print 'Running '+ str_cmd
            # evoke function
            cmd_tokens = re.split(r'[()]',str_cmd)
            module_name = cmd_tokens[0].replace('.py','')
            parameters = cmd_tokens[1].split(',')
            parameters = [convertType(parameters[i]) for i in range(len(parameters))] 
            if save ==1:
                np.save(log_fname_started,parameters)

            module = __import__(module_name)
            module.main(parameters)
            os.remove(log_fname_started)
            finish_log_id = open(log_fname_finished,'w')
            if save ==1: 
                np.save(log_fname_finished,parameters)
        elif len(varargin) == 1:
            sys.exit('length of varargin should be even number!')
        else:
            runExp(fname_command2+',', varargin,fname_prefix2, save = save)




save =1

try:
    opts, args=getopt.getopt(sys.argv[1:], "hm:p:s:",
            ["module_name=","parameters=","save:"])
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
    elif opt in("-s","--save="):
        save = int(arg)


random.seed(time.clock())
varargin_tokens = re.split(r'[\[\]]',parameters)[:-1]
runExp(module_name, varargin_tokens,fname_prefix=[],save=save)
'''    
    result_dir = '../Results/'
    if not os.isdir(result_dir):
        os.makedirs(result_dir)
    result = [hyp1,hyp2,hyp3]
    return result
    np.savetxt(result_dir+'hyp1_'+str(hyp1)+'_hyp2_'+str(hyp2)+'_hyp3_'+str(hyp3)+'_.csv',[hyp1,hyp2,hyp3],delimiter=',')
'''

