import psycopg2
import time
import sys
import stomp
import threading
import datetime
from commons import RandomUtils
from db_tools.postgresql import PG_Client


def readNewMessageFile():
    tag_info = PG_Client.query('select i_id from tag_info ORDER BY RANDOM() LIMIT 1 ', None);
    print(' rows : ', tag_info);
    msg = newMessageData(tag_info);
    print(' msg : ' , msg)


    with open('E:\projects\五系统一中心\mq_test\Win32\Win32\\001', 'w+') as f:
        f.write(str(msg));
        print(f.read())



def createNewMessage(count):
    allMsg = '';
    for i in range(count) :
        # 数据库查询
        tag_info = PG_Client.query('select i_id from tag_info ORDER BY RANDOM() LIMIT 1 ', None);
        print(' rows : ', tag_info);

        # 获取当前时间戳
        dtime = datetime.datetime.now()
        ans_time = int(time.mktime(dtime.timetuple())) * 1000;

        id = tag_info['i_id'];
        # id = 1111;
        # 图层
        emapArr = ['egms_369857' , 'egms_130738'];
        layer_name = RandomUtils.getRamdonByArr(emapArr);

        key = "coordinate"

        # 随机坐标
        x = RandomUtils.getRandomBetweenNumbers(0, 61);
        y = RandomUtils.getRandomBetweenNumbers(-46, 0);
        val = str(x) + "," + str(y);


        msg = '{"cls":"tag","id":%(id)d,"layer_name":"%(layer_name)s","time":%(time)d,"key":"%(key)s","val":"%(val)s"}\n';
        msg = msg % {   'id' : id ,
                        'layer_name' : layer_name ,
                        'time' : ans_time ,
                        'key'  : key ,
                        'val' : val
                     }
        allMsg += msg;

    print(' msg : ' , allMsg)
    with open('E:\projects\五系统一中心\mq_test\Win32\Win32\\001', 'w+') as f:
        f.write(allMsg)
        # f.write(writeMsg);
        # print(f.read())



def newMessageData(tag_info):
    # 图层
    emapArr = ['egms_map' , 'egms_461253' , 'egms_090836' ];

    mqMessageData = {};
    mqMessageData['cls'] = "tag"
    mqMessageData['id'] = tag_info['i_id'];
    # 随机获取图层
    layer_name = RandomUtils.getRamdonByArr(emapArr);
    mqMessageData['layer_name'] = layer_name
    mqMessageData['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mqMessageData['key'] = "coordinate"
    # 随机坐标
    x = RandomUtils.getRandomBetweenNumbers( 0 , 200  );
    y = RandomUtils.getRandomBetweenNumbers( -120 , 0 );
    mqMessageData['val'] = str(x) + "," + str(y);

    # key = RandomUtils.getRandomBetweenNumbers(0 , 10);
    # if key == 1 :
    #     mqMessageData['key'] = "online"
    #     mqMessageData['val'] = "0"

    # 自定义人数
    # personArr = [ 131 ,601 , 378 , 420  , 592]
    # mqMessageData['id'] = RandomUtils.getRamdonByArr(personArr);
    # mqMessageData['id'] = 300; # 321 130 128 300 601
    # mqMessageData['layer_name'] = 'egms_110'
    # 直接定义图层
    # mqMessageData['layer_name'] = 'egms_090836'
    # mqMessageData['key'] = "online"
    # mqMessageData['val'] = "0"
    # mqMessageData['key'] = "coordinate"
    # mqMessageData['val'] = str(328) + "," + str(10);
    return mqMessageData;





def writeNewMessageFile():
    tag_info = PG_Client.query('select i_id from tag_info ORDER BY RANDOM() LIMIT 1 ', None);
    print(' rows : ', tag_info);
    msg = newMessageData(tag_info);
    print(' msg : ' , msg)

    with open('E:\projects\五系统一中心\mq_test\Win32\Win32\\001', 'a+') as f:
        writeMsg =str(msg) + '\r'
        f.writelines(writeMsg)
        # f.write(writeMsg);
        print(f.read())




# for i in range(100):
#     writeNewMessageFile();

createNewMessage(15);



# 获取当前时间戳
dtime = datetime.datetime.now()
ans_time = int(time.mktime(dtime.timetuple())) ;

print('ans_time : '  , ans_time)



