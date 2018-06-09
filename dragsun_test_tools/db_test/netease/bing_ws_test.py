# 微软 必应 speech to text ws接口测试
import threading
import datetime
import time
from websocket import create_connection
from commons import utils

# https://github.com/websocket-client/websocket-client 官网

# 获取消息接收
class WsSelectorThread(threading.Thread):  # 继承父类threading.Thread
    wsClient = None;
    wsClientName = None;
    startListen = False;
    def __init__(self ):
        threading.Thread.__init__(self)

    def setWsClient(self , ws):
        self.wsClient = ws;
    def setWsClientName(self , name):
        self.wsClientName = name;

    def startListen(self):
        self.startListen = True;

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        while (True):
            if self.wsClient and self.startListen :
                result = self.wsClient.recv();
                print("ClientName : '%s' , Received '%s' " % (self.wsClientName , result ))
            print('拉取推送数据....')

def getUrl():
    connectionId = utils.getUUIDString();
    path = "wss://speech.platform.bing.com/speech/recognition/conversation/cognitiveservices/v1?format=detailed&language=en-US&Ocp-Apim-Subscription-Key=c9f881d1f5064db29c50588d5718946f&X-ConnectionId=";
    url = path + connectionId;
    return url;

def wsconnect():
    connectionId = 'netease_speech';
    uri = getUrl();
    ws = create_connection( uri ,
                           header={}
                           )

    status = ws.status;


    line_sep = '\r\n';
    requestid = utils.getUUIDString();
    timestamp = '2018-05-18T02:46:11.742Z';
    data1 = '';
    data1 = data1 + 'path: speech.config' + line_sep;
    data1 = data1 + 'x-requestid: ' + requestid + line_sep;
    data1 = data1 + 'x-timestamp: ' + timestamp + line_sep;
    data1 = data1 + 'content-type: application/json' + line_sep;
    data1 = data1 + line_sep;
    body = '{"context":{"system":{"version":"1.0.00000"},"os":{"platform":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36","name":"Browser","version":null},"device":{"manufacturer":"SpeechSample","model":"SpeechSample","version":"1.0.00000"}}}';
    data1 = data1 + body;
    ws.send(data1)


    # 创建新线程
    selectorThread = WsSelectorThread()
    clientName = 'ws客户端_: bing';
    selectorThread.setWsClientName(clientName);
    selectorThread.setWsClient(ws);
    selectorThread.startListen();
    selectorThread.start()

def test():

    print(utils.getUUIDString());


wsconnect()
