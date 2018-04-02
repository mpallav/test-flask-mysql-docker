#!/usr/bin/python
import re
import datetime
from datetime import timedelta
from pytz import timezone
import pytz
import argparse
import pdb
def countStr(filename,str_match):
    try:
       ''' insert escape characters to ensure exact match'''
       pattern='.+'+re.escape(str_match)+'.+' 
       pattern = re.compile(pattern,re.I)
       data = pattern.findall(filename)

    except (IOError,EOFError) as e:
       print 'multiple exception found' '''.format(e.args[-1])'''
    except ValueError as e:
       print 'Invalid value found'+str(e)
    else:
       return data   

def timeElapsed(data):
    ts_elapse = []
    ts_collect = []
    fmt = "%d/%b/%Y:%H:%M:%S" 
    try:
       '''get the timestamp'''
       for timestamp in data:
          ts = re.search('(\d{2}\/\w{3}\/\d{4}\:\d{2}\:\d{2}\:\d{2})',timestamp)
          if ts is not None:
                ts_collect.append(ts.group())
       '''get the timedelta'''
       if len(ts_collect) == 0:
          raise Exception ('no timestamp found')
	  return False,0,0
       if len(ts_collect)==1:
          avg=ts_collect[0]
          return True,ts_collect,avg
       else: 
          for i in range(1,len(ts_collect)):
             time2 = datetime.datetime.strptime(ts_collect[i], fmt)
             time1 = datetime.datetime.strptime(ts_collect[i-1], fmt)
             ts_elapse.append(time2 - time1)

       '''calculate the mean average of time elapsed'''
       avg = sum(ts_elapse,datetime.timedelta(0)) / len(ts_collect) 
    except ZeroDivisionError as e:
       print 'run time exception'+str(e)
       return False,0,0

    else:
       return True,ts_collect,avg


def utcToPstConvertor(ts_collect):

    newlog = []
    pst_time=[]
    '''get the timestamp'''
    fmt = "%d/%b/%Y:%H:%M:%S"
    newfmt = "%b %d %H:%M:%S"
    zone = 'US/Pacific'
    tz=pytz.timezone('UTC')
    tz_target=pytz.timezone(zone)

    for i in ts_collect:
       datetime_object = datetime.datetime.strptime(i,fmt)
       datetime_object=datetime_object.replace(tzinfo=tz)

       ''' convert timezone UTC to PST'''
       newtime = datetime_object.astimezone(tz_target)
       newtime=newtime.strftime(newfmt)
       ''' collect PST time string ''' 
       pst_time.append(newtime)
    return pst_time


def dumpLog(data,pst_time):
    '''log dump on screen'''
    for i, j in zip(data,pst_time):
       ts = re.sub('(^\w{3}\s\d{2}\s\d{2}\:\d{2}\:\d{2})',j,i)
       print ts
    return None

      
def main (filename,searchstring):
    try: 
       fd = open(filename,'r')

    except (IOError,EOFError) as e:
       print 'File corrupted or not found,'+str(e)
       return False
    fd=fd.read()
    data =  countStr(fd,searchstring)
    if not data:
       print 'No string match found'
       return False

    flag,ts_collect,avg= timeElapsed(data)
    if not flag: 
       return False 
    pst_time = utcToPstConvertor(ts_collect)
    if not pst_time:
       return False
    dumpLog(data,pst_time)
    print '\n\n**********************LOG SUMMRY*****************************'
    print 'Number of search string occurances: %d'%(len(data))
    print 'Mean time elapsed of string occurance: %s Seconds'%(str(avg.total_seconds()))
    return True 
 
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--file',type=str,dest='file',help='Enter the filename whose log needs to search',required=True)
    parser.add_argument('--searchstring',type=str,dest='searchstring', help='Enter the name of the string that needs to search',required=True)

    args = parser.parse_args()
    main (args.file,args.searchstring)
