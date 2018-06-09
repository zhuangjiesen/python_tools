
import time
import sys

print('参数个数为:', len(sys.argv), '个参数。')
print('参数列表:', str(sys.argv))

for i in range(0 , 6) :
    print ("Start : %s" % time.ctime());
    time.sleep( 5 )
    print ("end : %s" % time.ctime());
print(sys.argv[1] , '  python success ');




