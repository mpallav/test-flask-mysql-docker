#!/usr/bin/python
import re
import datetime
from datetime import timedelta
from pytz import timezone
import pytz
#from dateutil import tz
#from pytz import timezone
#import pytz
import argparse

def countStr(filename,str_match):
    try:
       pattern='.*'+str_match+'.*'
 
       if pattern is None:
          raise Exception('Input String match is none')

       pattern = re.compile(pattern)

       data= pattern.findall(filename)
    except (IOError,EOFError) as e:
       print 'multiple exception found' '''.format(e.args[-1])'''
    else:
       
       return len(data),data   

def timeElapsed(data):
    ts_elapse = []
    ts_collect = []
#[28/Nov/2016:19:19:48 +0000]
    try:
        '''get the timestamp'''
        for timestamp in data:
   
            ts = re.search('\[(\d{2}\/\w{3}\/\d{4}\:\d{2}\:\d{2}\:\d{2}).+\]',timestamp)
            #ts = re.search('^\w{3}\s\d{2}\s\d{2}\:\d{2}\:\d{2}',timestamp)
            if ts is not None:
                ts_collect.append(ts.group(1))
            else:
                raise Exception ('regex search string is Null')

        '''get the timedelta'''
        for i in range(len(ts_collect) - 1):
       
            if i > 0:
                time2 = datetime.datetime.strptime(ts_collect[i], "%d/%b/%Y:%H:%M:%S")
                #time2 = datetime.datetime.strptime(ts_collect[i], "%b %d %H:%M:%S")
                time1 = datetime.datetime.strptime(ts_collect[i-1], "%d/%b/%Y:%H:%M:%S")
                ts_elapse.append(time2 - time1)
           
    except ValueError as e:
        print 'value error found'+str(e)
   
    else:

        avg = sum(ts_elapse,datetime.timedelta(0)) / len(ts_collect) 
        return ts_collect,avg


def utcTOpstconvertor(ts_collect):
    newlog = []
    pstTime=[]
    '''get the timestamp'''
#    pst = timezone('US/Pacific')

    fmt = "%d/%b/%Y:%H:%M:%S"
    newfmt = "%b %d %H:%M:%S"
    zone = 'US/Pacific'
    tz=pytz.timezone('UTC')
    tz_target=pytz.timezone(zone)
    for i in ts_collect:
         datetime_object = datetime.datetime.strptime(i,fmt)
	 datetime_object=datetime_object.replace(tzinfo=tz)
#         print datetime_object
         newtime = datetime_object.astimezone(tz_target)
         newtime=newtime.strftime(newfmt) 
#	 print type(newtime)
         pstTime.append(newtime)
    return pstTime


def dumplog(data,pstTime):
  
    for i, j in zip(data,pstTime):
         ts = re.sub('(^\w{3}\s\d{2}\s\d{2}\:\d{2}\:\d{2})',j,i)
         print ts 
#         timeformat1 = datetime.datetime.strptime(ts.group(1), "%b %d %H:%M:%S")
#         dt_pst1 = timeformat1.astimezone(Local)
#         new_timezone1 = dt_pst1.strptime(dt_pst1, "%b %d %H:%M:%S")

#         timeformat2 = datetime.datetime.strptime(ts.group(2), "%d/%b/%Y:%H:%M:%S")
#         dt_pst2 = timeformat2.astimezone(Local)
#         new_timezone2 = dt_pst2.strptime(dt_pst2, "%d/%b/%Y:%H:%M:%S")
    
#         replace = str(new_timezone1)+' 
#         ts = re.sub('(^\w{3}\s\d{2}\s\d{2}\:\d{2}\:\d{2}).+(\d{2}\/\w{3}\/\d{4}\:\d{2}:\d{2}:\d{2})',(str(new_timezone1))+'.+'+(str(new_timezone2)),timestamp)
#         newlog.append(ts)

    return none
      
if __name__ == '__main__':

#    parser = argparse.ArgumentParser(description="prase argument filename and string to search occurances")
#    parser.add_argument('file', default='frontend-service.log',help='Enter the filename whose log needs to search')

#    parser.add_argument('name', help='Enter the name of the string that needs to search',type=str)

#    args = parser.parse_args()
    
     
#    fd = open(args.file,'r')
    fd = open('frontend-service.log','r')
    output=fd.read()
    
    name = raw_input('Enter the name string to search in log file: ')

    number,data =  countStr(output,name)


    print 'Occurance in countstr'
    print number
#    print data 
   
    ts_collect,avg= timeElapsed(data)
    print "Average time elapsed"
    print avg 
 
    pstTime = utcTOpstconvertor(ts_collect)
    dumplog(data,pstTime) 
