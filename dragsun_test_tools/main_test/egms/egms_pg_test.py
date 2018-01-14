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



# PG_Client.select('tag_point_record' , None , { 'tagid' : 121 } , None , [ 0 , 1]);
'''
随机查询一个标签
select * 
from tag_info ORDER BY RANDOM() 
LIMIT 1 

'''


# 发送Mq
conn = AmqConnetion();

# conn.startAndConnect();
conn.startAndConnectNotBack();



def newMessageData(tag_info):
    emapArr = ['egms_map' , 'egms_461253' , 'egms_090836' ];

    mqMessageData = {};
    mqMessageData['cls'] = "tag"
    mqMessageData['id'] = tag_info['i_id'];
    layer_name = RandomUtils.getRamdonByArr(emapArr);
    mqMessageData['layer_name'] = layer_name
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('time : ' , time) ;
    mqMessageData['time'] = time
    # mqMessageData['time'] = '2017-08-18 20:40:29'
    mqMessageData['key'] = "coordinate"
    x = RandomUtils.getRandomBetweenNumbers( 0 , 200  );
    y = RandomUtils.getRandomBetweenNumbers( -150 , 0 );
    mqMessageData['val'] = str(x) + "," + str(y);

    # key = RandomUtils.getRandomBetweenNumbers(0 , 10);
    # if key == 1 :
    #     mqMessageData['key'] = "online"
    #     mqMessageData['val'] = "0"

    # personArr = [ 131 ,601 , 378 , 420  , 592]
    # mqMessageData['id'] = RandomUtils.getRamdonByArr(personArr);
    # mqMessageData['id'] = 500; # 321 130 128 300 601
    # mqMessageData['id'] = 321; # 321 130 128 300 601
    mqMessageData['id'] = 503; # 321 130 128 300 601
    # mqMessageData['id'] = 368; # 321 130 128 300 601
    # mqMessageData['id'] = 365; # 321 130 128 300 601
    # mqMessageData['id'] = 558; # 321 130 128 300 601
    # mqMessageData['id'] = 59; # 321 130 128 300 601
    # mqMessageData['id'] = 25; # 321 130 128 300 601
    # mqMessageData['id'] = 476; # 321 130 128 300 601
    # mqMessageData['id'] = 106; # 321 130 128 300 601
    # mqMessageData['id'] = 152; # 321 130 128 300 601
    # mqMessageData['id'] = 417; # 321 130 128 300 601
    mqMessageData['layer_name'] = 'egms_458647'
    # mqMessageData['layer_name'] = 'egms_297556'
    print(' layer_name : ' , layer_name)
    mqMessageData['key'] = "online"
    mqMessageData['val'] = "0"
    # mqMessageData['key'] = "power"
    # mqMessageData['val'] =  RandomUtils.getRandomBetweenNumbers( 20 , 80 );


    # mqMessageData['key'] = "coordinate"
    # mqMessageData['val'] = str(328) + "," + str(-50);
    mqMessageData['anchorid'] = "1,2,3"

    return mqMessageData;


# 模拟来回走轨迹
def newGoBackRoll(tagid , srartX , startY ):
    mqMessageData = {};
    mqMessageData['cls'] = "tag"
    mqMessageData['id'] = tagid;
    mqMessageData['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mqMessageData['key'] = "coordinate"

    mqMessageData['val'] = str(srartX) + "," + str(startY);
    mqMessageData['layer_name'] = 'egms_090836'
    # mqMessageData['layer_name'] = 'egms_270291'
    mqMessageData['key'] = "online"
    mqMessageData['val'] = "0"
    mqMessageData['anchorid'] = "1,2,3"
    # mqMessageData['key'] = "power"
    # mqMessageData['val'] =  50;
    # mqMessageData['key'] = "sos"
    # mqMessageData['val'] = 1
    return mqMessageData;



def newSinglePersonMessageData(tag_info):
    emapArr = ['egms_map' , 'egms_461253' , 'egms_090836' ];

    mqMessageData = {};
    mqMessageData['cls'] = "tag"
    mqMessageData['id'] = tag_info['i_id'];
    layer_name = RandomUtils.getRamdonByArr(emapArr);
    mqMessageData['layer_name'] = layer_name
    mqMessageData['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mqMessageData['key'] = "coordinate"
    x = RandomUtils.getRandomBetweenNumbers( 0 , 200  );
    y = RandomUtils.getRandomBetweenNumbers( -120 , 0 );
    mqMessageData['val'] = str(x) + "," + str(y);

    key = RandomUtils.getRandomBetweenNumbers(0 , 10);
    # if key == 1 :
    #     mqMessageData['key'] = "online"
    #     mqMessageData['val'] = "0"

    mqMessageData['id'] = 1; # 321 130 128 300 601
    # mqMessageData['layer_name'] = 'egms_090836'
    mqMessageData['layer_name'] = 'egms_270291'
    # print(' layer_name : ' , layer_name)
    # mqMessageData['time'] = '2017-08-02 11:31:13'
    # mqMessageData['time'] = '2017-08-02 11:33:05'
    # mqMessageData['key'] = "online"
    # mqMessageData['val'] = "0"

    # mqMessageData['key'] = "power"
    # mqMessageData['val'] =  50;

    # mqMessageData['key'] = "sos"
    # mqMessageData['val'] = 1

    # mqMessageData['key'] = "coordinate"
    # mqMessageData['val'] = str(328) + "," + str(-30);
    return mqMessageData;




def newSOSMessageData(tag_info):
    mqMessageData = {};
    mqMessageData['cls'] = "tag"
    mqMessageData['id'] = tag_info['i_id'];
    # personArr = [ 131 ,601 , 378 , 420  , 592]
    # mqMessageData['id'] = 592 ; # 321
    mqMessageData['layer_name'] = "egms_461253"
    mqMessageData['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mqMessageData['key'] = "sos"
    mqMessageData['val'] = 1
    return mqMessageData;

def newPowerMessageData(tag_info):
    mqMessageData = {};
    mqMessageData['cls'] = "tag"
    # mqMessageData['id'] = tag_info['i_id'];
    mqMessageData['id'] = 592 ; # 321

    personArr = [ 131 ,601 , 378 , 420  , 592]
    mqMessageData['id'] = RandomUtils.getRamdonByArr(personArr);
    mqMessageData['layer_name'] = "egms_110"
    mqMessageData['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mqMessageData['key'] = "power"
    mqMessageData['val'] =  RandomUtils.getRandomBetweenNumbers( 20 , 80  );
    return mqMessageData;



def newOnlineMessageData(tag_info):
    mqMessageData = {};
    mqMessageData['cls'] = "tag"
    # mqMessageData['id'] = tag_info['i_id'];
    personArr = [ 131 ,601 , 378 , 420  , 592]

    mqMessageData['id'] = 592 ; # 321
    mqMessageData['layer_name'] = "egms_461253"
    mqMessageData['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mqMessageData['key'] = "online"
    mqMessageData['val'] = 1
    return mqMessageData;

# 定位数据
def sendLocationMsg():
    for i in range(1) :
        # tag_info = PG_Client.query('select i_id from tag_info ORDER BY RANDOM() LIMIT 1 ', None);
        tag_info = PG_Client.query('select i_id from tag_info ORDER BY RANDOM() LIMIT 1 ', None);
        print(' rows : ', tag_info);
        message = newMessageData(tag_info);
        print(' message : ', message);
        conn.sendTopic(str(message) , 'testtopic');




# 线程保活
class LocationMessageThread(threading.Thread):  #
    def __init__(self ):
        threading.Thread.__init__(self)

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        sendLocationMsg();



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


# 上下线数据
def sendOnlineMsg():
    for i in range(1) :
        tag_info = PG_Client.query('select * from tag_info ORDER BY RANDOM() LIMIT 1 ', None);
        print(' rows : ', tag_info);
        message = newOnlineMessageData(tag_info);
        conn.sendTopic(str(message) , 'testtopic');





def sendSOSMsg():
    for i in range(2000) :
        tag_info = PG_Client.query('select * from tag_info ORDER BY RANDOM() LIMIT 1 ', None);
        print(' rows : ', tag_info);
        message = newSOSMessageData(tag_info);
        print(' message : ', message);

        conn.sendTopic(str(message) , 'testtopic');

def sendPowerMsg():
    for i in range(10) :
        tag_info = PG_Client.query('select * from tag_info ORDER BY RANDOM() LIMIT 1 ', None);
        print(' rows : ', tag_info);
        message = newPowerMessageData(tag_info);
        conn.sendTopic(str(message) , 'testtopic');


def sendSinglePersonLocationMsg():
    for i in range(1000) :
        tag_info = PG_Client.query('select * from tag_info ORDER BY RANDOM() LIMIT 1 ', None);
        print(' rows : ', tag_info);
        message = newSinglePersonMessageData(tag_info);
        conn.sendTopic(str(message) , 'testtopic');

def sendGoBackRollLocationMsg(id , startX , startY ):
    startX = 20;
    startY = -50
    for i in range(20) :
        message = newGoBackRoll(id ,startX , startY );
        startX = startX + 5;
        conn.sendTopic(str(message) , 'testtopic');

    for i in range(20) :
        message = newGoBackRoll(id ,startX , startY );
        startX = startX - 5;
        conn.sendTopic(str(message) , 'testtopic');





def newOnlyOneMessageData(tag_info):
    mqMessageData = {};
    mqMessageData['cls'] = "tag"
    # mqMessageData['id'] = tag_info['i_id'];
    mqMessageData['id'] = 587; # 587 32
    mqMessageData['layer_name'] = "egms_110"
    mqMessageData['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mqMessageData['key'] = "coordinate"
    mqMessageData['val'] = "55,-78888"
    # mqMessageData['key'] = "online"
    # mqMessageData['val'] = 0
    return mqMessageData;




# sendOnlineMsg();



# sendSOSMsg();
# sendPowerMsg();
# sendOnlyOne();
sendLocationMsg()
# sendSinglePersonLocationMsg()
# sendGoBackRollLocationMsg();





# message = newMessageData();
# conn.sendTopic(str(message), 'testtopic');

# conn.sendQueue('zhuangjiesenhahahahahah' , 'hellomq');

'''

conn.setQueueConsumer('hellomq' , MyMsgListener())
conn.setTopicConsumer('hellomqTopic' , MyTopicMsgListener())
class MyMsgListener(MessageListener):
    def on_message(self, headers, message):
        print('---MyMsgListener---on_message----------')

    def on_error(self, headers, message):
        print('---MyMsgListener----on_error---------')

class MyTopicMsgListener(MessageListener):
    def on_message(self, headers, message):
        print('---MyTopicMsgListener---on_message----------')

    def on_error(self, headers, message):
        print('---MyTopicMsgListener----on_error---------')

'''

