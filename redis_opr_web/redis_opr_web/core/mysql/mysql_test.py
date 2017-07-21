from ..mysql import MysqlClient

# res = mysql_client.queryBySql('SELECT * from app_redis ');
# print(' res : ' , res);


arr = ['a' , 'b' , 'c'];
res = MysqlClient.query('app_redis', [
    'i_id', 'app_name'
], { 'i_id' : 26 }, { 'i_id' : 'desc' }, [0  ,2 ])
print(' query res : ' , res);

# res = mysql_client.getTableCols('app_redis');
# print(' getTableCols res : ' , res);


# res = mysql_client.checkTableCols('app_redis' , {'remark' : 'xxx' , 'location' : 'xxx' , 'i_id' : 2});
# print(' checkTableCols res : ' , res);


# res = mysql_client.alter_add_new_col('app_redis' , 'lccation' , 255);
# print(' checkTableCols res : ' , res);




res = MysqlClient.insert('app_redis', {'app_name' : 'redis_python'});
print(' checkTableCols res : ' , res);




# res =mysql_client.update('app_redis' , 'i_id' , 26 , { 'app_name' : '333'})
# print(' checkTableCols res : ' , res);