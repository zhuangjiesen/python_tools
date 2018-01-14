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

conn.startAndConnect();


emapList = ["egms_578270" ,
"egms_279079" ,
"egms_180827" ,
'egms_559769',
'egms_578270',
'egms_279079',
'egms_180827',
'egms_370126',
'egms_359938',
'egms_323903',
'egms_203280',
'egms_254808',
'egms_532733',
'egms_218147',
'egms_346795',
'egms_468756',
'egms_451088'

            ];


def sendOnlineMessage(tagid):
    print('发送上线消息');
    levelName = RandomUtils.getRamdonByArr(emapList);
    mqMessageData = {};
    mqMessageData['cls'] = "tag"
    mqMessageData['id'] = tagid;
    mqMessageData['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mqMessageData['key'] = "coordinate"
    mqMessageData['val'] = str(10) + "," + str(-10);
    mqMessageData['layer_name'] = 'egms_532733'
    mqMessageData['anchorid'] = '1,3';
    message = str(mqMessageData)
    print('message : ' , message)
    conn.sendTopic(message, 'testtopic');
    return mqMessageData;


'''
更新表关联关系
'''
def updatePersonId():
    '''
    计算总数
    select count(1)
    from door_person_info dpi
    left join  tag_info ti  on dpi.i_person_id = ti.c_person_id and ti.i_id = dpi.i_tag_id
    where ti.i_id is null
    '''
    total = 1150;
    pageSize = 500;
    page = total / pageSize + 1;
    page = int(page);
    '''
    select dpi.*
    from door_person_info dpi
    left join  tag_info ti  on dpi.i_person_id = ti.c_person_id and ti.i_id = dpi.i_tag_id
    where ti.i_id is null
    
    
    select ti.i_id ,  ti.c_person_id 
    from tag_info ti  
    left join  
    door_person_info dpi  on dpi.i_person_id = ti.c_person_id and ti.i_id = dpi.i_tag_id 
    where dpi.i_person_id  is null order by dpi.i_person_id  desc  


    '''
    for pageNo in range(0 , page) :
        offset = pageNo * pageSize;
        sql = 'select dpi.i_person_id , dpi.i_tag_id ' \
              'from door_person_info dpi ' \
              'left join  tag_info ti  ' \
              'on dpi.i_person_id = ti.c_person_id' \
              ' and ti.i_id = dpi.i_tag_id ' \
              'where ti.i_id is null' \
              ' order by dpi.i_person_id desc ' \
              ' limit ' + str(pageSize) + ' offset ' + str(offset) + '' ;


        tag_info_sql = ' select ti.i_id ,  ti.c_person_id ' \
                       'from tag_info ti ' \
                       'left join door_person_info dpi  ' \
                       'on dpi.i_person_id = ti.c_person_id ' \
                       'and ti.i_id = dpi.i_tag_id ' \
                       'where dpi.i_person_id  is null ' \
                       'order by dpi.i_person_id  desc  ' \
                       ' limit ' + str(pageSize) + ' offset ' + str(offset) + '' ;

        personList = PG_Client.query(sql , None);
        tagInfoList = PG_Client.query(tag_info_sql , None);

        i = 0;
        if personList and len(personList) :
            conn = PG_Client.getConn();
            cur = conn.cursor();
            for personItem in personList :
                tagInfoItem = tagInfoList[i];
                tagid = tagInfoItem['i_id'];
                i_person_id = personItem['i_person_id']
                '''
                update tag_info set c_person_id = %s
                where i_id = %s
                '''
                updateSql = ' update tag_info set c_person_id = %s ' \
                            'where i_id = %s';
                updatePersonSql = ' update door_person_info set i_tag_id = %s ' \
                            'where i_person_id = %s';
                params = [];
                params.append(i_person_id)
                params.append(tagid)
                personParams = [];
                personParams.append(tagid)
                personParams.append(i_person_id)
                cur.execute(updateSql, tuple(params));
                cur.execute(updatePersonSql, tuple(personParams));
                i = i + 1;
            conn.commit()
            cur.close()
            conn.close()



def getTagListByPages(pageNo):
    total = 10081;
    pageSize = 500;
    offset = ( pageNo - 1 ) * pageSize;
    tagInfoSql = 'select * ' \
                 'from tag_info ' \
                 'order by i_id asc  ' \
                 ' limit ' + str(pageSize) + ' offset ' + str(offset) + '';
    tagInfoList = PG_Client.query(tagInfoSql, None);
    return tagInfoList


def sendLocationData(tagid):
    print('发送上线消息');
    levelName = RandomUtils.getRamdonByArr(emapList);
    mqMessageData = {};
    mqMessageData['cls'] = "tag"
    mqMessageData['id'] = tagid;
    mqMessageData['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mqMessageData['key'] = "coordinate"
    x = RandomUtils.getRandomBetweenNumbers(100 , 40000)
    y = RandomUtils.getRandomBetweenNumbers(-20000 ,-100 )
    mqMessageData['val'] = str(x) + "," + str(y);
    mqMessageData['layer_name'] = levelName
    mqMessageData['anchorid'] = '1111,1131';
    message = str(mqMessageData)
    print('message : ' , message)
    conn.sendTopic(message, 'testtopic');
    return mqMessageData;



