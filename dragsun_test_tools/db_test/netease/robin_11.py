

# 知更数据库脚本
from  db_tools.mysql import  MysqlClient
from  db_tools.mysql import  MysqlStatusCheck
from commons import RandomUtils
from commons import utils
from redis_tools import RedisCluster
from redis_tools import RedisClient
import time
import datetime

print ("...")
def insertByBatch_SubjectInfo():
    for i in range(1 , 2000):
        subject_info = {};
        name = 'subject_info_test_name_' + str(i);
        subject_info['subject_id'] = i;
        subject_info['name'] = name;
        subject_classification_id = RandomUtils.getRandomBetweenNumbers(0 , 10)
        subject_info['subject_classification_id'] = subject_classification_id;
        alias =  'subject_info_test_alias_' + str(i);
        desc =  'subject_info_test_desc_' + str(i);
        remark =  'subject_info_test_remark_' + str(i);
        subject_info['alias'] = alias;



        subject_info['desc'] = desc;
        subject_info['link_url'] = 'http://axure.yixin.im/view?pid=10&mid=82&id=2887#%E9%A6%96%E9%A1%B5-%E5%85%B3%E6%B3%A8';
        subject_info['title_img_url'] = 'http://axure.yixin.im/view?pid=10&mid=82&id=2887#%E9%A6%96%E9%A1%B5-%E5%85%B3%E6%B3%A8';
        subject_info['status'] = '1';
        subject_info['db_create_time'] = RandomUtils.getLimitRandomTime();
        subject_info['remark'] = remark;
        subject_info['type'] = '1';
        subject_info['db_update_user'] = 1;
        updateTime = RandomUtils.getLimitRandomTime();
        subject_info['db_update_time'] = updateTime;
        subject_info['subject_key'] = RandomUtils.getRandomStr(30);


        print (subject_info)
        res = MysqlClient.insert('subject_info' , subject_info);
        print ('res : ' , res);




def insertByBatch_user_follow_subject():
    subject_id = 7;
    for i in range(30 , 40):
        user_follow_subject = {};
        user_follow_subject['id'] = i;
        user_follow_subject['user_id'] = 'zhuangjiesen';
        user_follow_subject['subject_id'] = subject_id;
        user_follow_subject['db_create_time'] = RandomUtils.getRandomTodayTime()
        user_follow_subject['db_update_time'] = RandomUtils.getRandomTodayTime()
        user_follow_subject['status'] = '1';
        user_follow_subject['subject_key'] = '0';
        subject_id = subject_id + 1;
        res = MysqlClient.insert('user_follow_subject' , user_follow_subject);
        print ('res : ' , res);




def insertByBatch_EventInfo():
    for i in range(1 , 20):
        event_info = {};
        name = 'event_info_test_name_' + str(i);
        event_info['event_id'] = i;
        event_info['event_name'] = name;
        desc =  'sevent_info_test_desc_' + str(i);
        remark =  'event_info_test_remark_' + str(i);

        event_info['desc'] = desc;
        event_info['remark'] = remark;

        event_info['img_url'] = 'http://axure.yixin.im/view?pid=10&mid=82&id=2887#%E9%A6%96%E9%A1%B5-%E5%85%B3%E6%B3%A8';
        event_info['status'] = '1';
        event_info['db_create_time'] = RandomUtils.getLimitRandomTime();
        updateTime = RandomUtils.getLimitRandomTime();
        event_info['db_update_time'] = updateTime;
        event_info['article_update_time'] = RandomUtils.getLimitRandomTime();


        print (event_info)
        res = MysqlClient.insert('event_info' , event_info);
        print ('res : ' , res);



def insertByBatch_index_range_info():
    id = 200;
    for subject_id in range(0, 2001):
        list = MysqlClient.query('subject_info', ['*'], {'subject_id': subject_id}, {'subject_id': 'ASC'}, None);
        if list and len(list) > 0:
            subject_info = list[0]
            index_range_info = {};
            index_range_info['id'] = id;
            index_range_info['range_type'] = '1';
            index_range_info['range_obj_id'] = subject_info['subject_id'];
            index_range_info['article_update_time_long'] =utils.switchTimeToLong(RandomUtils.getLimitRandomTime());
            index_range_info['article_update_count'] = 10;
            index_range_info['db_create_time'] =  RandomUtils.getLimitRandomTime();
            index_range_info['db_update_time'] =  RandomUtils.getLimitRandomTime();
            index_range_info['range_obj_key'] = '0';
            res = MysqlClient.insert('index_range_info', index_range_info);
        id = id + 1;
    for feeds_id in range(0, 283):
        list = MysqlClient.query('sys_feeds_info', ['*'], {'id': feeds_id}, {'id': 'ASC'}, None);
        if list and len(list) > 0:
            feeds_info = list[0]
            index_range_info = {};
            index_range_info['id'] = id;
            index_range_info['range_type'] = '0';
            index_range_info['range_obj_id'] = '0';
            index_range_info['article_update_time_long'] = utils.switchTimeToLong(RandomUtils.getLimitRandomTime());
            index_range_info['article_update_count'] = 10;
            index_range_info['db_create_time'] = RandomUtils.getLimitRandomTime();
            index_range_info['db_update_time'] = RandomUtils.getLimitRandomTime();
            index_range_info['range_obj_key'] = feeds_info['feeds_key'];
            res = MysqlClient.insert('index_range_info', index_range_info);
        id = id + 1;



def insertByBatch_keyword_subject_classification_info():
    for i in range(1 , 20):
        event_info = {};
        name = 'event_info_test_name_' + str(i);
        event_info['event_id'] = i;
        event_info['event_name'] = name;
        desc =  'sevent_info_test_desc_' + str(i);
        remark =  'event_info_test_remark_' + str(i);

        event_info['desc'] = desc;
        event_info['remark'] = remark;

        event_info['img_url'] = 'http://axure.yixin.im/view?pid=10&mid=82&id=2887#%E9%A6%96%E9%A1%B5-%E5%85%B3%E6%B3%A8';
        event_info['status'] = '1';
        event_info['db_create_time'] = RandomUtils.getLimitRandomTime();
        updateTime = RandomUtils.getLimitRandomTime();
        event_info['db_update_time'] = updateTime;
        event_info['article_update_time'] = RandomUtils.getLimitRandomTime();


        print (event_info)
        res = MysqlClient.insert('event_info' , event_info);
        print ('res : ' , res);



def insertByBatch_keyword_info():
    for i in range(1 , 100):
        keyword_info = {};
        name = 'keyword_info_关键词_' + str(i);
        keyword_info['keyword_id'] = i;
        keyword_info['name'] = name;
        keyword_info['score'] = '0';
        keyword_info['subject_id'] = RandomUtils.getRandomBetweenNumbers(1 , 10);
        keyword_info['status'] = '1';
        keyword_info['db_create_time'] = RandomUtils.getLimitRandomTime();
        updateTime = RandomUtils.getLimitRandomTime();
        keyword_info['db_update_time'] = updateTime;
        print (keyword_info)
        res = MysqlClient.insert('keyword_info' , keyword_info);
        print ('res : ' , res);



def insertByBatch_keyword_relate_article():
    for i in range(1 , 30):
        # 文章数量
        articleCount = RandomUtils.getRandomBetweenNumbers(2 , 10);
        for c in range (0 , articleCount) :
            keyword_relate_article = {};
            keyword_relate_article['keyword_id'] = i;
            result = MysqlClient.queryBySql('select article_id from article_source_info order by rand() limit 1 ;');
            keyword_relate_article['article_id'] = result[0]['article_id'];
            keyword_relate_article['db_create_time'] = RandomUtils.getLimitRandomTime();
            updateTime = RandomUtils.getLimitRandomTime();
            keyword_relate_article['db_update_time'] = updateTime;
            print (keyword_relate_article)
            res = MysqlClient.insert('keyword_relate_article' , keyword_relate_article);
            print ('res : ' , res);



def insertByBatch_keyword_subject_classification_info():
    for i in range(1 , 100):
        # 文章数量
        keyid = RandomUtils.getRandomBetweenNumbers(1 , 30);
        name = 'keyword_info_关键词_' + str(keyid);
        keyword_subject_classification_info = {};
        keyword_subject_classification_info['key_sbj_clsf_id'] = i;
        keyword_subject_classification_info['keyword_name'] = name;
        keyword_subject_classification_info['subject_id'] = RandomUtils.getRandomBetweenNumbers(1 , 10);
        keyword_subject_classification_info['sbj_classification_id'] = RandomUtils.getRandomBetweenNumbers(1 , 5 );
        keyword_subject_classification_info['is_contain'] = '1';
        keyword_subject_classification_info['word_status'] = '1';
        keyword_subject_classification_info['relate_score'] = '1';
        keyword_subject_classification_info['status'] = '1';
        keyword_subject_classification_info['db_create_time'] = RandomUtils.getLimitRandomTime();
        updateTime = RandomUtils.getLimitRandomTime();
        keyword_subject_classification_info['db_update_time'] = updateTime;
        print(keyword_subject_classification_info)
        res = MysqlClient.insert('keyword_subject_classification_info', keyword_subject_classification_info);
        print('res : ', res);



def updateUpdateTime():
    for id in range(0 , 35):
        updateTime = RandomUtils.getLimitRandomTime();

        subject_info = {};
        subject_info['db_update_time'] = updateTime;
        res = MysqlClient.update('subject_info' , 'subject_id' , id , subject_info);
        print ('res : ' , res);



def updateArticleSourceInfo():
    for article_id in range(0 , 420):
        list = MysqlClient.query('article_source_info', ['*'], {'article_id': article_id}, {'article_id': 'ASC'}, None);
        if list and len(list) > 0:
            article_info = list[0]

            article_info_update = {};
            # article_info_update['subject_id'] = RandomUtils.getRandomBetweenNumbersStr(1 , 50);

            today = RandomUtils.getRandomTodayTime();
            article_info_update['publish_date'] = today;
            article_info_update['db_update_time'] = today;
            article_info_update['db_create_time'] = today;

            res = MysqlClient.update('article_source_info' , 'article_id' , article_id , article_info_update);


def updateIndexRangeInfoArticleCount():
    for index_id in range(0 , 2483):
        list = MysqlClient.query('index_range_info', ['*'], {'id': index_id}, {'id': 'ASC'}, None);
        if list and len(list) > 0:
            index_range_info = list[0]
            range_type = index_range_info['range_type']
            if range_type == '0':
                # 订阅源
                feeds_key = index_range_info['range_obj_key'];
                sql = " SELECT COUNT(1) as count FROM article_source_info WHERE feeds_key = '" + feeds_key + "'";
                res = MysqlClient.queryBySql(sql);
                if res and len(res) > 0:
                    item = res[0]
                    if utils.containsKey(item , 'count') :
                        count = item['count'];
                        index_range_info_update = {};
                        index_range_info_update['article_update_count'] = count;
                        index_range_info_update['article_update_time_long'] = utils.switchTimeToLong(
                            RandomUtils.getRandomTodayTime());
                        res = MysqlClient.update('index_range_info', 'id', index_id, index_range_info_update);
                    else:
                        index_range_info_update = {};
                        index_range_info_update['article_update_count'] = 0;
                        index_range_info_update['article_update_time_long'] = utils.switchTimeToLong(
                            RandomUtils.getRandomTodayTime());
                        res = MysqlClient.update('index_range_info', 'id', index_id, index_range_info_update);

            else:
                subject_id = index_range_info['range_obj_id'];
                sql = " SELECT COUNT(1) as count FROM article_source_info WHERE subject_id = '" + str(subject_id) + "'";
                res = MysqlClient.queryBySql(sql);
                if res and len(res) > 0:
                    item = res[0]
                    if utils.containsKey(item, 'count'):
                        count = item['count'];
                        index_range_info_update = {};
                        index_range_info_update['article_update_count'] = count;
                        index_range_info_update['article_update_time_long'] = utils.switchTimeToLong(
                            RandomUtils.getRandomTodayTime());
                        res = MysqlClient.update('index_range_info', 'id', index_id, index_range_info_update);
                    else:
                        index_range_info_update = {};
                        index_range_info_update['article_update_count'] = 0;
                        index_range_info_update['article_update_time_long'] = utils.switchTimeToLong(
                            RandomUtils.getRandomTodayTime());
                        res = MysqlClient.update('index_range_info', 'id', index_id, index_range_info_update);


def updateSubjectImageUrl():
    print()
    imageUrlList = [];
    imageUrlList.append('https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=2031009439,2234982214&fm=200&gp=0.jpg');
    imageUrlList.append('https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=1822586924,1495363676&fm=27&gp=0.jpg');
    imageUrlList.append('https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=471934028,1076887700&fm=27&gp=0.jpg');
    imageUrlList.append('http://img4.imgtn.bdimg.com/it/u=1835461009,3758533189&fm=200&gp=0.jpg');
    imageUrlList.append('http://img5.imgtn.bdimg.com/it/u=3962409022,1822913369&fm=27&gp=0.jpg');
    imageUrlList.append('http://img1.imgtn.bdimg.com/it/u=174844028,3129694553&fm=27&gp=0.jpg');
    imageUrlList.append('http://img2.imgtn.bdimg.com/it/u=678379141,306910345&fm=27&gp=0.jpg');
    imageUrlList.append('http://img5.imgtn.bdimg.com/it/u=1574237258,862097733&fm=27&gp=0.jpg');
    imageUrlList.append('http://img0.imgtn.bdimg.com/it/u=1009667019,2713680909&fm=27&gp=0.jpg');
    imageUrlList.append('http://img2.imgtn.bdimg.com/it/u=2863483125,754535105&fm=27&gp=0.jpg');
    imageUrlList.append('http://img3.imgtn.bdimg.com/it/u=665457040,754967999&fm=27&gp=0.jpg');
    imageUrlList.append('http://img3.imgtn.bdimg.com/it/u=3762633794,2242939757&fm=200&gp=0.jpg');
    imageUrlList.append('http://img0.imgtn.bdimg.com/it/u=1509826265,2253101521&fm=27&gp=0.jpg');
    imageUrlList.append('http://img4.imgtn.bdimg.com/it/u=3263114642,1353411666&fm=27&gp=0.jpg');
    imageUrlList.append('http://img3.imgtn.bdimg.com/it/u=2555685737,1386930382&fm=200&gp=0.jpg');
    for id in range(0 , 2001):
        updateTime = RandomUtils.getLimitRandomTime();
        imageUrl = RandomUtils.getRamdonByArr(imageUrlList);
        subject_info = {};
        subject_info['title_img_url'] = imageUrl;
        res = MysqlClient.update('subject_info' , 'subject_id' , id , subject_info);
        print ('res : ' , res);


def updateEventImageUrl():
    print()
    imageUrlList = [];
    imageUrlList.append('http://img2.imgtn.bdimg.com/it/u=3611229455,3568603237&fm=27&gp=0.jpg');
    imageUrlList.append('http://img2.imgtn.bdimg.com/it/u=1482298243,1338134557&fm=27&gp=0.jpg');
    imageUrlList.append('http://img1.imgtn.bdimg.com/it/u=300576743,3174238928&fm=27&gp=0.jpg');
    imageUrlList.append('http://img4.imgtn.bdimg.com/it/u=3052125567,2171710751&fm=27&gp=0.jpg');
    imageUrlList.append('http://img1.imgtn.bdimg.com/it/u=81350360,2957301497&fm=27&gp=0.jpg');
    imageUrlList.append('http://img5.imgtn.bdimg.com/it/u=12590684,1477161663&fm=27&gp=0.jpg');
    imageUrlList.append('http://img2.imgtn.bdimg.com/it/u=933039219,1837158407&fm=27&gp=0.jpg');
    imageUrlList.append('http://img0.imgtn.bdimg.com/it/u=3330600848,2100253034&fm=27&gp=0.jpg');
    imageUrlList.append('http://img5.imgtn.bdimg.com/it/u=603849291,3946710276&fm=27&gp=0.jpg');
    imageUrlList.append('http://img5.imgtn.bdimg.com/it/u=4138413863,1656628636&fm=27&gp=0.jpg');
    imageUrlList.append('http://img2.imgtn.bdimg.com/it/u=2797783117,2599030229&fm=27&gp=0.jpg');
    imageUrlList.append('http://img5.imgtn.bdimg.com/it/u=2860768968,1152669767&fm=27&gp=0.jpg');
    imageUrlList.append('http://img1.imgtn.bdimg.com/it/u=1225908358,945448395&fm=27&gp=0.jpg');
    imageUrlList.append('http://img5.imgtn.bdimg.com/it/u=1576088825,3183834070&fm=27&gp=0.jpg');
    imageUrlList.append('http://img0.imgtn.bdimg.com/it/u=1442301841,2270688881&fm=27&gp=0.jpg');
    for id in range(0 , 20):
        updateTime = RandomUtils.getLimitRandomTime();
        imageUrl = RandomUtils.getRamdonByArr(imageUrlList);
        event_info = {};
        event_info['img_url'] = imageUrl;
        res = MysqlClient.update('event_info' , 'event_id' , id , event_info);
        print ('res : ' , res);

def testMediaFileToRedis():
    print()



# updateUpdateTime();
# 批量生成 专题数据
# insertByBatch_SubjectInfo();
# insertByBatch_EventInfo();
# insertByBatch_index_range_info();
updateArticleSourceInfo();
updateIndexRangeInfoArticleCount();
# insertByBatch_user_follow_subject();
# insertByBatch_keyword_info();
# insertByBatch_keyword_relate_article();
# insertByBatch_keyword_subject_classification_info();
# updateSubjectImageUrl();
# updateEventImageUrl();



# 把专题信息加载redis
def loadSubjectDataIntoRedis():
    rs_client = RedisClient.createRedisConn("127.0.0.1", 6379, "redis");
    res = rs_client.redisClient.info();
    for subject_id in range(0 , 2001 ):
        list = MysqlClient.query('subject_info' , ['*'] , {'subject_id' : subject_id } , { 'subject_id' : 'ASC'} , None);
        if list and len(list) > 0 :
            subject_info = list[0]
            print(str(subject_info))
            data = str(subject_info);
            res = rs_client.redisClient.hset('subject_info_all' , str(subject_id) , data);

        # score = RandomUtils.getRandomBetweenNumbers(152358337 * 1000 , 202358337 * 1000)
        # res = rs_client.redisClient.zadd('subject_info_range' , str(subject_id) , score);
    print (res)

# loadSubjectDataIntoRedis();



def loadSubjectDataArticleListIntoRedis():
    rs_client = RedisClient.createRedisConn("127.0.0.1", 6379, "redis");
    res = rs_client.redisClient.info();
    for subject_id in range(0 , 2001 ):
        list = MysqlClient.query('subject_info' , ['*'] , {'subject_id' : subject_id } , { 'subject_id' : 'ASC'} , None);
        if list and len(list) > 0 :
            id1 = RandomUtils.getRandomBetweenNumbers( 10 , 3000 )
            id2 = RandomUtils.getRandomBetweenNumbers( 10 , 3000 )
            id3 = RandomUtils.getRandomBetweenNumbers( 10 , 3000 )

            score1 = RandomUtils.getRandomBetweenNumbers(152358337 * 1000, 202358337 * 1000)
            score2 = RandomUtils.getRandomBetweenNumbers(152358337 * 1000, 202358337 * 1000)
            score3 = RandomUtils.getRandomBetweenNumbers(152358337 * 1000, 202358337 * 1000)

            key = 'subject_article_range_zset_prefix:' + str(subject_id);
            res = rs_client.redisClient.zadd(key , id1 , score1, id2 , score2 , id3 , score3  );
            randomNum = RandomUtils.getRandomBetweenNumbers(0 , 1);
            if randomNum == 0:
                id4 = RandomUtils.getRandomBetweenNumbers(10, 3000)
                score4 = RandomUtils.getRandomBetweenNumbers(152358337 * 1000, 202358337 * 1000)

                res = rs_client.redisClient.zadd(key, id4, score4 );




    print (res)

# loadSubjectDataArticleListIntoRedis();


# feedsinfo_article_range_zset_prefix:



def loadFeedsArticleListIntoRedis():
    rs_client = RedisClient.createRedisConn("127.0.0.1", 6379, "redis");
    res = rs_client.redisClient.info();
    for feeds_id in range(0 , 282 ):
        list = MysqlClient.query('sys_feeds_info' , ['*'] , {'id' : feeds_id } , { 'id' : 'ASC'} , None);
        if list and len(list) > 0 :
            feeds_info = list[0];
            feeds_key = feeds_info['feeds_key'];
            id1 = RandomUtils.getRandomBetweenNumbers( 10 , 3000 )
            id2 = RandomUtils.getRandomBetweenNumbers( 10 , 3000 )
            id3 = RandomUtils.getRandomBetweenNumbers( 10 , 3000 )

            score1 = RandomUtils.getRandomBetweenNumbers(152358337 * 1000, 202358337 * 1000)
            score2 = RandomUtils.getRandomBetweenNumbers(152358337 * 1000, 202358337 * 1000)
            score3 = RandomUtils.getRandomBetweenNumbers(152358337 * 1000, 202358337 * 1000)
            key = 'feedsinfo_article_range_zset_prefix:' + str(feeds_key);
            res = rs_client.redisClient.zadd(key , id1 , score1, id2 , score2 , id3 , score3  );
            randomNum = RandomUtils.getRandomBetweenNumbers(0 , 1);
            if randomNum == 0:
                id4 = RandomUtils.getRandomBetweenNumbers(10, 3000)
                score4 = RandomUtils.getRandomBetweenNumbers(152358337 * 1000, 202358337 * 1000)

                res = rs_client.redisClient.zadd(key, id4, score4 );




    print (res)

# loadFeedsArticleListIntoRedis();

# 时间转换
def timeSwitch(dateStr):
    timeArray = time.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    timeStamp = timeStamp * 1000;
    return timeStamp;



# 加载更新列表
def loadFeedsUpdateRangeToRedis():
    rs_client = RedisClient.createRedisConn("127.0.0.1", 6379, "redis");
    res = rs_client.redisClient.info();
    for feeds_id in range(0 , 282 ):
        list = MysqlClient.query('sys_feeds_info' , ['*'] , {'id' : feeds_id } , { 'id' : 'ASC'} , None);
        if list and len(list) > 0 :
            feeds_info = list[0];
            feeds_key = feeds_info['feeds_key'];
            cache_prefix = 'feeds_:';
            id = cache_prefix + feeds_key;

            db_update_time = feeds_info['db_update_time'];
            timeLong = timeSwitch(db_update_time);


            key = 'subject_feeds_info_updatetime_range_zset';
            count = rs_client.redisClient.zcount(key ,timeLong ,timeLong );
            while count > 0 :
                timeLong = timeLong + 1;
                count = rs_client.redisClient.zcount(key, timeLong, timeLong);

            score = timeLong;
            res = rs_client.redisClient.zadd(key , id , score );

    print()
def loadSubjectUpdateRangeToRedis():
    rs_client = RedisClient.createRedisConn("127.0.0.1", 6379, "redis");
    res = rs_client.redisClient.info();
    for subject_id in range(0 , 2001 ):
        list = MysqlClient.query('subject_info' , ['*'] , {'subject_id' : subject_id } , { 'subject_id' : 'ASC'} , None);
        if list and len(list) > 0 :
            subject_info = list[0];

            cache_prefix = 'subject_:';
            id = cache_prefix + str(subject_info['subject_id']);

            db_update_time = subject_info['db_update_time'];
            timeLong = timeSwitch(db_update_time);
            score = timeLong;
            key = 'subject_feeds_info_updatetime_range_zset';

            count = rs_client.redisClient.zcount(key ,timeLong ,timeLong );
            while count > 0 :
                timeLong = timeLong + 1;
                count = rs_client.redisClient.zcount(key, timeLong, timeLong);

            res = rs_client.redisClient.zadd(key , id , score );

    print()


# loadFeedsUpdateRangeToRedis();
# loadSubjectUpdateRangeToRedis();


# print(timeSwitch('2018-02-24 10:35:55'));
