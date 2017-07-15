import time
import sys
import stomp
import threading
import datetime
from commons import RandomUtils
from mq_tools.amq import Amq_Conf

# 线程保活
class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self ):
        threading.Thread.__init__(self)

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        while True:
            time.sleep(5)
            # print(" thread starting ....")





# 全局无法对 destination 分别设置consumer 用一个路由类分发
class MessageListenerRoute(object):
    messageListenerDict = None;

    def __init__(self) -> None:
        super().__init__()
        self.messageListenerDict  = {};

    def addMessageListener(self, subscribe):
        type = subscribe.type;
        # 前缀 queue or topic
        destinationPrefix = Amq_Conf.DESTINATION_TYPE[type];
        destination = '' + destinationPrefix + subscribe.targetDestination;
        self.messageListenerDict[destination] = subscribe.listener;


    def on_error(self, headers, message):
        print('received an error %s' % message)
        destination = headers['destination'];
        # 查找是否设置监听
        if containsKey(self.messageListenerDict , destination) :
            messageListener = self.messageListenerDict[destination]
            messageListener.on_error(headers, message);
        else:
            print('not a listener of destination  %s' % destination)


    def on_message(self, headers, message):
        print('received a message %s' % message)
        destination = headers['destination'];
        # 查找是否设置监听
        if containsKey(self.messageListenerDict , destination) :
            messageListener = self.messageListenerDict[destination]
            messageListener.on_message(headers, message);
        else:
            print('not a listener of destination  %s' % destination)


class MessageListener(object):
    def on_error(self, headers, message):
        print('received an error %s' % message)
    def on_message(self, headers, message):
        print('received a message %s' % message)

class Subscribe:
    # 0 queue 1 topic
    type = None;
    targetDestination = None;
    listener = None;


class AmqConnetion:
    conn = None;
    messageListenerRoute = None;
    subscribeList = [];

    def __init__(self) -> None:
        super().__init__()
        self.conn = stomp.Connection10([(Amq_Conf.HOST, Amq_Conf.PORT)])
        self.messageListenerRoute = MessageListenerRoute();
        # 注册全局消息监听路由
        self.conn.set_listener('messageListenerRoute', self.messageListenerRoute)

    # 开启服务并开启保活线程
    def startAndConnect(self):
        # 开启服务
        self.startAndConnectIsBackThread(True)

    # 开启服务 程序跑完就死亡
    def startAndConnectNotBack(self):
        # 开启服务
        self.startAndConnectIsBackThread(False)


    def startAndConnectIsBackThread(self , isBack):
        # 开启服务
        self.conn.start()
        self.conn.connect()
        if isBack :
            # 创建新线程 使程序持续运行
            thread2 = myThread()
            # 开启线程
            thread2.start()

        # 遍历注册消费者
        if len(self.subscribeList) > 0 :
            for subItem in self.subscribeList :
                type = subItem.type;
                descTypeStr = Amq_Conf.DESTINATION_TYPE[type];
                # 要监听的目的地
                destination = subItem.targetDestination;
                listenDesc = '' + descTypeStr + destination;
                print(' subscribe : ' , listenDesc)
                self.conn.subscribe(destination=listenDesc, id=1, ack='auto')

    def sendQueue(self , content, targetDestination):
        des = Amq_Conf.QUEUE + targetDestination
        # print(' destination : ' , des)
        self.conn.send(body=str(content), content_type='text/plain;charset=utf-8', destination=des )


    def sendTopic(self ,content, targetDestination):
        print()
        des = Amq_Conf.TOPIC + targetDestination
        self.conn.send(body=str(content), content_type='text/plain;charset=utf-8', destination=des )


    # 注册队列消费者
    def setQueueConsumer(self , destination , listener):
        subscribe = Subscribe();
        # queue类型
        subscribe.type = 0;
        subscribe.listener = listener;
        subscribe.targetDestination = destination;
        self.messageListenerRoute.addMessageListener(subscribe)
        self.subscribeList.append(subscribe)


    # 注册 topic 消费者
    def setTopicConsumer(self , destination , listener):
        subscribe = Subscribe();
        # topic 类型
        subscribe.type = 1;
        subscribe.listener = listener;
        subscribe.targetDestination = destination;
        self.messageListenerRoute.addMessageListener(subscribe)
        self.subscribeList.append(subscribe)


def containsKey(dict , key):
    if not dict :
        return False;
    if key in dict.keys():
        return True;