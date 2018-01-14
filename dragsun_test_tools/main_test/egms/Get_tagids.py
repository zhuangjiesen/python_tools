import psycopg2
import time
import sys
import stomp
import threading
import datetime
from commons import RandomUtils
from db_tools.postgresql import PG_Client



with open('E:\projects\五系统一中心\mq_test\\tagid.txt', 'w+') as f:
    pageNo = 1;
    pageSize = 20;


    # 10081
    # 分页查询标签
    while (pageNo < 600) :
        offSet = (pageNo - 1) * pageSize;


        if pageNo % 60 == 0 :
            f.write('\n');
            f.write('\n');
            f.write('\n');
            f.write('\n');

        sql = 'select i_id from tag_info ORDER BY i_id asc limit %(pageSize)s offset %(offset)d ';
        sql = sql % {'pageSize': pageSize,
                     'offset': offSet
                     }
        tag_info_list = PG_Client.query(sql, None);

        message = '';
        if tag_info_list and len(tag_info_list) > 0 :
            for tagItem in tag_info_list :
                i_id = tagItem['i_id'];
                message = message + str(i_id) ;
                message = message + ',';

        print('tag_info_list : ', tag_info_list);
        pageNo = pageNo + 1;
        f.write(message);
        f.write('\n');
        print(f.read())



