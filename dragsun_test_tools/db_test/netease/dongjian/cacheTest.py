from redis_tools import RedisClient
import codecs


def tempHtmlPagesCache():
    rs_client = RedisClient.createRedisConn("127.0.0.1" , 6379 , "redis");
    res = rs_client.redisClient.info();

    fd = codecs.open('/Users/zhuangjiesen/netease/dongjian/dev/dongjian-ms-internal/dongjian-ms-internal/src/main/resources/mail-template/companyAuth.html')
    htmlContent = fd.read();
    print('sql : %s ' % (htmlContent))

    rs_client.redisClient.set('htmlContent' , htmlContent)
    print(res);

tempHtmlPagesCache();