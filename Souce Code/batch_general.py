# Usage:
# make sure that the Project Template folder structure is followed.  
# In terminal run:  python batch_general.py -m tempCode -p 'p1 [ BB, UCF101] p2 [3, 1]'
# Note:
#   -m flag model name, the model has to have the code in def main()
#   -p flag parameters which is passed in as one single string variable. each hyperparameter name is followed by a list of values in a pire of [] separated by space. The values in the lists are separated by ','.  
#   -s save parameter to log file. 1: save, o.w.:don't save
#   -e send email when each grid is finished. 1: send, o.w.: don't send
#   -t reciever's email address
#   -f sender's email address
#   string variable values can be in pairs of '' or "" or none.
#   Log file use the naming convention that each token is separated by '_' so avoid naming variables using '_'
#   Parameters are stored in both the start and finish log file. If the parameter has large volume, use -s 0 flag to supress saving.
 
# Example: 
# python batch_general.py -m tempCode -p 'p1 [ BB, UCF101] p2 [3, 1]'
# Example 2:
# python batch_general.py -m tempCode -p 'p1 [ "BB", "UCF101"] p2 [3, 1]'
# The code support empty argument



import subprocess
import smtplib
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
from email.mime.text import MIMEText

def convertType(var):
    try:
        return  int(var)
    except:
        try:
            return float(var)
        except:
            return var

def runExp(fname_command, varargin,fname_prefix=[],save = 1,email=1,toAddr=[],fromAddr=[],):

    if len(fname_prefix) ==0:
        Log_dir = './Log/'
        if not os.path.isdir(Log_dir):
            os.makedirs(Log_dir)
        fname_prefix = './Log/'+fname_command
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
            module_name = cmd_tokens[0]
            parameters = cmd_tokens[1].split(',')
            parameters = [convertType(parameters[i]) for i in range(len(parameters))] 
            if save ==1:
                np.save(log_fname_started,parameters)
 
            # execute main file
            module = __import__(module_name)
            starttime = time.time()
            module.main(parameters)
            exe_time = time.time()-starttime 
            os.remove(log_fname_started)
            print str_cmd+' is finished. Using '+str(exe_time)+' seconds.'
            finish_log_id = open(log_fname_finished,'w')
            if email != 0:
                str_subject = str_cmd+' has finished.\n\n'
                hostname = subprocess.Popen('hostname', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()[0]
                screen_id = subprocess.Popen('echo $STY', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()[0]
                win_id = subprocess.Popen('echo $WINDOW', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()[0]
                str_content = 'Job finished. \nHost: '+hostname+'Screen: '+screen_id+'Window: '+str(win_id)+'\n'+'Using '+str(exe_time)+' seconds.\n'
                if save == 1:
                    str_content = str_content+'Parameters has been saved to '+log_fname_finished+'\n'
                msg = MIMEText(str_content)
                msg["To"] = toAddr
                msg["From"] = fromAddr
                msg["Subject"] = str_subject
                p = subprocess.Popen(["sendmail","-t","oi"],stdin=subprocess.PIPE)
                p.communicate(msg.as_string())
            if save ==1: 
                np.save(log_fname_finished,parameters)
        elif len(varargin) == 1:
            sys.exit('length of varargin should be even number!')
        else:
            runExp(fname_command2+',', varargin,fname_prefix2, save = save,email=email,toAddr = toAddr,fromAddr = fromAddr)




save =1
email = 1
toAddr = 'yeliu.system.mail@gmail.com'
fromAddr = []
try:
    opts, args=getopt.getopt(sys.argv[1:], "hm:p:s:e:t:f:",
            ["module_name=","parameters=","save=","email=","toAddr=","fromAddr="])
except getopt.GetoptError:
    print 'gae_demo.py -i <inputfile>'
    sys.exit(2)

for opt, arg in opts:
    if opt =='-h':
        exit()
    elif opt in("-m","--module_name="):
        module_name = arg.replace('.py','')
    elif opt in("-p","--parameters="):
        parameters = arg
    elif opt in("-s","--save="):
        save = int(arg)
    elif opt in("-e","--email="):
        email = int(arg)
    elif opt in("-t","--toAddr="):
        toAddr = arg
    elif opt in("-f","--fromAddr="):
        fromAddr = arg

random.seed(time.clock())
varargin_tokens = re.split(r'[\[\]]',parameters)[:-1]

runExp(module_name, varargin_tokens,fname_prefix=[],save=save,email = email,toAddr = toAddr,fromAddr = fromAddr)
'''    
    result_dir = '../Results/'
    if not os.isdir(result_dir):
        os.makedirs(result_dir)
    result = [hyp1,hyp2,hyp3]
    return result
    np.savetxt(result_dir+'hyp1_'+str(hyp1)+'_hyp2_'+str(hyp2)+'_hyp3_'+str(hyp3)+'_.csv',[hyp1,hyp2,hyp3],delimiter=',')
'''

