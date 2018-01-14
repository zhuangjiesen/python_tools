from  db_tools.mysql import  MysqlClient
from  db_tools.mysql import  MysqlStatusCheck

# res = mysql_client.queryBySql('SELECT * from app_redis ');
# print(' res : ' , res);


# arr = ['a' , 'b' , 'c'];
# res = MysqlClient.query('m_user', None ,  None , None , [0  ,2 ])
# print(' query res : ' , res);



# res = MysqlClient.executeSql('  show index from m_user; ' , None) ;
# print(' 1.query res : ' , res);

# tableColumns = MysqlClient.showTableColumns('goods');
# print(' 3.query res : ' , tableColumns);
# if tableColumns :
#     for colItem in tableColumns :
#         field = colItem['Field'];

# res = MysqlClient.executeSql('  select count(goods_id) as total , goods_name  from goods group by goods_name ' , None) ;
# print(' 4.query res : ' , res);

# res = MysqlClient.queryBySql('  select count(goods_id) as total from goods ');
# print(' 5.query res : ' , res);

# res = MysqlClient.queryBySql(' explain select count(goods_id) as total from goods ');
# print(' 6.query res : ' , res);



# res = MysqlStatusCheck.getDataLength('goods') ;
# print(' 6.query res : ' , res);



res = MysqlStatusCheck.getSlowLogOfSql('goods') ;
print(' 6.query res : ' , res);


# res = MysqlStatusCheck.getExplainOfSql('select count(goods_id) as total from goods ') ;
# print(' 6.query res : ' , res);

# res = MysqlClient.showTableIndexInfo('goods');
# print(' 7.query res : ' , res);




# res = MysqlStatusCheck.getIndexSelectable('goods');
# print(' 8.query res : ' , res);


# res = MysqlStatusCheck.getColumnsSelectable('goods');
# print(' 8.query res : ' , res);

# res = mysql_client.getTableCols('app_redis');
# print(' getTableCols res : ' , res);


# res = mysql_client.checkTableCols('app_redis' , {'remark' : 'xxx' , 'location' : 'xxx' , 'i_id' : 2});
# print(' checkTableCols res : ' , res);


# res = mysql_client.alter_add_new_col('app_redis' , 'lccation' , 255);
# print(' checkTableCols res : ' , res);




# res = MysqlClient.insert('app_redis', {'app_name' : 'redis_python'});
# print(' checkTableCols res : ' , res);




# res =mysql_client.update('app_redis' , 'i_id' , 26 , { 'app_name' : '333'})
# print(' checkTableCols res : ' , res);