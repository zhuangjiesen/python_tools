import datetime
import time

dtime = datetime.datetime.now()
ans_time = int(time.mktime(dtime.timetuple())) * 1000;

print('dtime : ' , dtime)
print('ans_time : ' , ans_time)




print('-----------------------' )