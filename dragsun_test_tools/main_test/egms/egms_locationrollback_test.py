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




# 发送Mq
conn = AmqConnetion();

# conn.startAndConnect();
conn.startAndConnectNotBack();


# 模拟来回走轨迹
def newGoBackRoll(tagid , srartX , startY ):
    mqMessageData = {};
    mqMessageData['cls'] = "tag"
    mqMessageData['id'] = tagid;
    mqMessageData['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mqMessageData['key'] = "coordinate"

    mqMessageData['val'] = str(srartX) + "," + str(startY);
    # mqMessageData['layer_name'] = 'egms_090836'
    mqMessageData['layer_name'] = 'egms_158282'
    # mqMessageData['key'] = "online"
    # mqMessageData['val'] = "0"
    # mqMessageData['key'] = "power"
    # mqMessageData['val'] =  50;
    # mqMessageData['key'] = "sos"
    # mqMessageData['val'] = 1
    return mqMessageData;



# 线程保活
class LocationMessageThread(threading.Thread):  #
    def __init__(self ):
        threading.Thread.__init__(self)

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print()



'''
# 创建新线程 使程序持续运行
thread1 = LocationMessageThread()
# 开启线程
thread1.start()
thread2 = LocationMessageThread()
# 开启线程
thread2.start()
thread3 = LocationMessageThread()
# 开启线程
thread3.start()

thread4 = LocationMessageThread()
# 开启线程
thread4.start()


thread5 = LocationMessageThread()
# 开启线程
thread5.start()

thread6 = LocationMessageThread()
# 开启线程
thread6.start()

thread7 = LocationMessageThread()
# 开启线程
thread7.start()

thread8 = LocationMessageThread()
# 开启线程
thread8.start()

'''


def sendGoBackRollLocationXMsg(id , startX , startY , steps ):

    print('sendGoBackRollLocationXMsg : ..........')
    for i in range(steps) :
        message = newGoBackRoll(id ,startX , startY );
        startX = startX + 5;
        conn.sendTopic(str(message) , 'testtopic');

    for i in range(steps) :
        message = newGoBackRoll(id ,startX , startY );
        startX = startX - 5;
        conn.sendTopic(str(message) , 'testtopic');




def sendGoBackRollLocationYMsg(id, startX, startY, steps):

    print('sendGoBackRollLocationYMsg : ..........')

    for i in range(steps):
        message = newGoBackRoll(id, startX, startY);
        startY = startY - 5;
        conn.sendTopic(str(message), 'testtopic');

    for i in range(steps):
        message = newGoBackRoll(id, startX, startY);
        startY = startY + 5;
        conn.sendTopic(str(message), 'testtopic');



'''
tagArray = [];
startX = 20;
startY = -50
tagid = 1;

tagObj = {};
tagObj['startX'] = startX;
tagObj['startY'] = startY;
tagObj['tagid'] = tagid;
tagObj['isX'] = True;
tagArray.append(tagObj);


tagObj = {};
startX = 20;
startY = -10
tagid = 2;
tagObj['startX'] = startX;
tagObj['startY'] = startY;
tagObj['tagid'] = tagid;
tagObj['isX'] = False;
tagArray.append(tagObj);

tagObj = {};
startX = 60;
startY = -10
tagid = 3;
tagObj['startX'] = startX;
tagObj['startY'] = startY;
tagObj['tagid'] = tagid;
tagObj['isX'] = False;
tagArray.append(tagObj);
'''



# tagArray = [];
# tag_arr = PG_Client.query('select i_id from tag_info ORDER BY RANDOM() LIMIT 2 ', None);
# tag_arr = PG_Client.query('select i_id from tag_info ORDER BY i_id  LIMIT 2 ', None);
# for i in range(len(tag_arr)) :
#     tagItem = tag_arr[i]
#     startX = 20;
#     startY = -10;
#     key = RandomUtils.getRandomBetweenNumbers(0 , 2);
#     isX = False
#     if key == 1 :
#         # x 移动
#         startX = startX + (i * 3)
#         isX = True;
#     else:
#         startY = startY - (i - 3)
#
#     tagObj = {};
#     tagid = tagItem['i_id'];
#     tagObj['startX'] = startX;
#     tagObj['startY'] = startY;
#     tagObj['tagid'] = tagid;
#     tagObj['isX'] = isX;
#     tagArray.append(tagObj);

# sendGoBackRollLocationArrayMsg( tagArray , 10)
# print('tag_arr : ' , tag_arr)


'''
    tagid = 300;
    startX = 20;
    startY = -50
    for i in range(50):
        message = newGoBackRoll(tagid, startX, startY);
        startX = startX + 5;
        conn.sendTopic(str(message), 'testtopic');
        time.sleep(0.05)

    for i in range(50):
        message = newGoBackRoll(tagid, startX, startY);
        startX = startX - 5;
        conn.sendTopic(str(message), 'testtopic');
        time.sleep(0.05)
'''

def sendGoBackRollLocationArrayMsg( tagid  , startX ,startY , isX ,  steps):
    for i in range(steps):
        message = newGoBackRoll(tagid, startX, startY);
        if isX :
            startX = startX + 5;
        else:
            startY = startY - 5;
        conn.sendTopic(str(message), 'testtopic');
        time.sleep(0.005)

    for i in range(steps):
        message = newGoBackRoll(tagid, startX, startY);
        if isX :
            startX = startX - 5;
        else:
            startY = startY + 5;
        conn.sendTopic(str(message), 'testtopic');
        time.sleep(0.005)






# 线程保活
class OneThread(threading.Thread):  # 继承父类threading.Thread
    tagid = 300;
    startX = 20;
    startY = -50
    isX = True;
    def __init__(self ):
        threading.Thread.__init__(self)

    def setParams (self , tagid , startX , startY , isX):
        self.tagid = tagid;
        self.startX = startX;
        self.startY = startY
        self.isX = isX;

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        sendGoBackRollLocationArrayMsg(self.tagid  , self.startX  ,self.startY , self.isX  , 30);


tagid = 300
for i in range(10) :
    tagid = tagid + i + 5
    startY = 10 + i * 10;
    startY = -startY;
    # 创建新线程
    thread2 = OneThread()
    thread2.setParams(tagid , 20 , startY , True );
    thread2.setDaemon(False);
    # 开启线程
    thread2.start()


####  下面是上下活动


tagid = 450
for i in range(10) :
    tagid = tagid + i + 5
    startX = 10 + i * 20;
    # 创建新线程
    thread2 = OneThread()
    thread2.setParams(tagid , startX , -10 , False );
    thread2.setDaemon(False);
    # 开启线程
    thread2.start()




# 线程保活
# class TwoThread(threading.Thread):  # 继承父类threading.Thread
#     def __init__(self ):
#         threading.Thread.__init__(self)
#
#     def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
#         while True:
#             time.sleep(5)
#             print(" thread starting ....")





# 创建新线程
# thread3 = TwoThread()
# thread3.setDaemon(False);
# # 开启线程
# thread3.start()




# 线程保活
# class ThreeThread(threading.Thread):  # 继承父类threading.Thread
#     def __init__(self ):
#         threading.Thread.__init__(self)
#
#     def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
#         while True:
#             time.sleep(5)
#             print(" thread starting ....")





# 创建新线程
# thread4 = ThreeThread()
# thread4.setDaemon(False);
# # 开启线程
# thread4.start()




