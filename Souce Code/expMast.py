import numpy as np
import os
import re
import pylab as pl
import sys
import getopt

def runExp(modul_name,parameters,start_log_id,finish_log_id):

    print 'Module: '+module_name+' Parameters: '+  parameters


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


start_log_name = '../Results/start_log.txt'
finish_log_name = '../Results/finish_log.txt'
start_log_id = open(start_log_name,'a')
finish_log_id = open(finish_log_name,'a')


runExp(module_name,parameters,start_log_id,finish_log_id)

'''    
    result_dir = '../Results/'
    if not os.isdir(result_dir):
        os.makedirs(result_dir)
    result = [hyp1,hyp2,hyp3]
    return result
    np.savetxt(result_dir+'hyp1_'+str(hyp1)+'_hyp2_'+str(hyp2)+'_hyp3_'+str(hyp3)+'_.csv',[hyp1,hyp2,hyp3],delimiter=',')
'''

