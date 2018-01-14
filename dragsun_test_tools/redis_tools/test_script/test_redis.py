# 链接redis 并存入数据库
from redis_tools import RedisCluster
from redis_tools import RedisClient
from commons import RandomUtils


rs_client = RedisClient.createRedisConn("192.168.130.130" , 6379 , "redis");
def testHash():
    for i in range(0 , 30000) :
        mStr =  RandomUtils.getRandomStr(10000);
        print(' str : ' , mStr);
        rs_client.redisClient.hset("delMap" , str(i) , mStr );

def testString():
    for i in range(0 , 300000) :
        mStr =  RandomUtils.getRandomStr(10000);
        key = 'testKey_:_' + str(i);
        # print(' str : ' , mStr);
        rs_client.redisClient.set(key , mStr);
testString();
res = RedisClient.getServer(rs_client)
print(' res : ' , res)




