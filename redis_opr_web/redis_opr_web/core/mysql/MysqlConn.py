import pymysql;
from DBUtils.PooledDB import PooledDB;

from ..mysql import MysqlConf as Config;

'''
@功能：PT数据库连接池
'''
class PTConnectionPool(object):
    __pool = None;



    def __init__(self):
        self.conn = self.getConn();
        print ("PT数据库创建con和cursor");

    def getConn(self):
        if self.__pool is None:
            self.__pool = PooledDB(creator=pymysql, mincached=Config.DB_MIN_CACHED , maxcached=Config.DB_MAX_CACHED,
                                   maxshared=Config.DB_MAX_SHARED, maxconnections=Config.DB_MAX_CONNECYIONS,
                                   blocking=Config.DB_BLOCKING, maxusage=Config.DB_MAX_USAGE,
                                   setsession=Config.DB_SET_SESSION,
                                   host=Config.DB_TEST_HOST , port=Config.DB_TEST_PORT ,
                                   user=Config.DB_TEST_USER , passwd=Config.DB_TEST_PASSWORD ,
                                   db=Config.DB_TEST_DBNAME , use_unicode=True, charset=Config.DB_CHARSET);

        return self.__pool.connection()

    def getCursor(self):
        return self.conn.cursor();

    """
    @summary: 释放连接池资源
    """
    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()

        print ("PT连接池释放con和cursor");

