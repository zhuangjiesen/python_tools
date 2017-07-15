import time
import sys
import stomp
import threading
import datetime
from commons import RandomUtils

class MyListener(object):
    def on_error(self, headers, message):
        print('received an error %s' % message)
        print('received an headers %s' % headers)
    def on_message(self, headers, message):
        print('received a message %s' % message)
        print('received an headers %s' % headers)
        destination = headers['destination'];
        print(' destination  %s' % destination)




#官方示例的连接代码也落后了，现在分协议版本
conn = stomp.Connection10([('10.11.165.11',61613)])
conn.set_listener('hellomq', MyListener())

conn.start()
conn.connect()

conn.subscribe(destination='/queue/hellomq', id=1, ack='auto')


# 线程保活
class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self ):
        threading.Thread.__init__(self)

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        while True:
            time.sleep(5)
            print(" thread starting ....")


# 创建新线程
thread2 = myThread()
# 开启线程
thread2.start()
