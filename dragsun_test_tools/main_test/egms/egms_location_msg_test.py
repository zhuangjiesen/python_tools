import psycopg2
import time
import sys
import stomp
import threading
import datetime
from commons import RandomUtils
from db_tools.postgresql import PG_Client
from mq_tools.amq import Amq_Conn
from mq_tools.amq.Amq_Conn import MessageListener
from mq_tools.amq.Amq_Conn import AmqConnetion
from main_test.egms import  egms_location_msg_fun as locationMsgUtils


print('发送消息 .....')

'''
total = 10081;
pageSize = 100;
page = int(total/pageSize) + 1;
page = int(page)
for pageNo in range(1 , page) :
    tagInfoList = locationMsgUtils.getTagListByPages(pageNo);
    if tagInfoList and len(tagInfoList) > 0 :
        for tagInfoItem in tagInfoList:
            i_id = tagInfoItem['i_id']
            locationMsgUtils.sendOnlineMessage(i_id);
'''



# 线程保活
class OneThread(threading.Thread):  # 继承父类threading.Thread
    tagInfoList = None;
    def __init__(self ):
        threading.Thread.__init__(self)

    def setParams (self ,tagInfoList):
        self.tagInfoList = tagInfoList;

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        tagInfoList = self.tagInfoList;
        while (True):
            if tagInfoList and len(tagInfoList) > 0:
                for tagInfoItem in tagInfoList:
                    i_id = tagInfoItem['i_id']
                    locationMsgUtils.sendLocationData(i_id);
            else:
                return;
            print('第一轮消息发送成功。。。')
            time.sleep(5)



total = 10081;
pageSize = 500;
page = int(total / pageSize) + 1;
page = int(page)
for pageNo in range(1, page):
    tagInfoList = locationMsgUtils.getTagListByPages(pageNo);
    print(' page : ' , page , ' 线程')
    # 创建新线程
    thread2 = OneThread()
    thread2.setParams(tagInfoList);
    # 开启线程
    thread2.start()


print('发送完毕')
# locationMsgUtils.sendOnlineMessage();


