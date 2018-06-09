# 链接redis 并存入数据库
from redis_tools import RedisCluster
from redis_tools import RedisClient
from commons import RandomUtils



datasize = 1024 * 100;
rs_client = RedisClient.createRedisConn("127.0.0.1" , 6379 , "redis");
def testHash():
    for i in range(0 , 3000) :
        mStr =  RandomUtils.getRandomStr(datasize);
        print(' str : ' , mStr);
        rs_client.redisClient.hset("delMap" , str(i) , mStr );

def testString():
    for i in range(0 , 300000) :
        mStr =  RandomUtils.getRandomStr(1024*100);
        key = 'testKey_:_' + str(i);
        # print(' str : ' , mStr);
        rs_client.redisClient.set(key , mStr);

def testList():
    key = 'testKey_:_list';
    for i in range(0, 30000):
        mStr = RandomUtils.getRandomStr(1024);
        # print(' str : ' , mStr);
        rs_client.redisClient.lpush(key, mStr);
# testString();
# testHash();
testList();
res = RedisClient.getServer(rs_client)
print(' res : ' , res)


