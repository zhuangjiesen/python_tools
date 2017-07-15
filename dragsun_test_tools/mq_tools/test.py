
#注意，官方示例这样发送消息是有问题的
#conn.send(body='hello,garfield! this is '.join(sys.argv[1:]), destination='/queue/test')
# conn.send(body='hello,garfield!' , content_type='text/plain;charset=utf-8', destination='/queue/testmq')
# conn.send(body={'name' : 'zhuangjiesen' , 'content' : '我是庄杰森'}, destination='/queue/testmq')
# conn.send('/topic/SampleTopic', 'Simples Assim')

# print('-------------')
# time.sleep(2)
# conn.disconnect()



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
# thread2.start()

class TagLocationRecord:
    id = None;
    tagid = None;
    x = None;
    y = None;
    lat = None;
    lon = None;
    speed = None;
    status = None;
    tagName = None;
    levelName = None;
    emapId = None;
    department = None;
    personId = None;
    personName = None;
    personTel = None;
    anchorId = None;
    locatedTime = None;
    locatedTimeStart = None;
    type  = None;
    power  = None;
    isSos = None;
    isOnline = None;
    createTime = None;
    updateTime = None;
    def toDict(self):
        dict = {};
        dict['success'] = self.success
        dict['msg'] = self.msg
        dict['result'] = self.result
        return dict;


def createNewTagLocationRecord():
    record = TagLocationRecord();
    record.tagName = 'xxxx';
    return record;

data = createNewTagLocationRecord().__dict__

'''
{"cls":"tag","id":23,"layer_name":"egms_110","time":1499751639,"key":"online","val":1}
{"cls":"tag","id":23,"layer_name":"egms_110","time":1499751639,"key":"coordinate","val":"1,-4830"}
{"cls":"tag","id":23,"layer_name":"egms_110","time":1499751639,"key":"coordinate","val":"1,-4830"}
{"cls":"tag","id":23,"layer_name":"egms_110","time":1499751639,"key":"coordinate","val":"1,-4830"}
{"cls":"tag","id":23,"layer_name":"egms_110","time":1499751639,"key":"power","val":80}
{"cls":"tag","id":23,"layer_name":"egms_110","time":1499751639,"key":"sos","val":0}
{"cls":"tag","id":23,"layer_name":"egms_110","time":1499751639,"key":"online","val":1}
'''

print(str(data))
# 发消息

# conn.send(body= str(data), content_type='aplication/json;charset=utf-8', destination='/queue/testmq')
mqMessage = '{"cls":"tag","id":23,"layer_name":"egms_110","time":1499751639,"key":"online","val":1}';

def newMessageData():
    mqMessageData = {};
    mqMessageData['cls'] = "tag"
    mqMessageData['id'] = RandomUtils.getRandomBetweenNumbers(0 , 1000)
    mqMessageData['layer_name'] = "egms_110"
    mqMessageData['time'] = 1499751639
    mqMessageData['key'] = "coordinate"
    mqMessageData['val'] = "1,-4830"
    return mqMessageData;

# for i in range(1000) :
#     # mqMessage = '{"cls":"tag","id":23,"layer_name":"egms_110","time":1499751639,"key":"coordinate","val":"1,-4830"}'
#     conn.send(body=str(newMessageData()), content_type='text/plain;charset=utf-8', destination='/queue/testmq')
# fromTime = datetime.datetime.now().second;
# for i in range(5000) :
#     msg = newMessageData();
#     print('newMessageData : ' ,msg )
#     conn.send(body=str(msg), content_type='text/plain;charset=utf-8', destination='/topic/testtopic')
# disTime = datetime.datetime.now().second - fromTime;
# print('disTime : ' , disTime)