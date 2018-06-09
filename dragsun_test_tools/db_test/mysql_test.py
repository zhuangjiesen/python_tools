
from  db_tools.mysql import  MysqlClient
from  db_tools.mysql import  MysqlStatusCheck

# 添加 创建时间和更新时间字段
# 查询数据库下的表目录
sql = "select table_name from information_schema.tables where table_schema='robins-1' and table_type='base table';";

res = MysqlClient.executeSql(sql , None) ;
print(' 1.query res : ' , res);
for item in res :
    table_name = item['table_name'];
    is_create_time_exist = MysqlClient.hasTableCols(table_name,'db_create_time' );
    if not is_create_time_exist :
        # 添加 db_create_time 字段
        sql = " alter table " + table_name + " add db_create_time timestamp " ;
        print ("sql : " , sql )
        res = MysqlClient.queryBySql(sql);
        print (" db_create_time : " , res )


    is_update_time_exist = MysqlClient.hasTableCols(table_name,'db_update_time' );
    if not is_update_time_exist :
        # 添加 db_update_time 字段
        sql = " alter table " + table_name + " add db_update_time timestamp " ;
        print ("sql : " , sql )
        res = MysqlClient.queryBySql(sql);
        print (" db_update_time : " , res )

    print('.....' , table_name)
    print('is_create_time_exist : ' , is_create_time_exist)
    print('is_update_time_exist : ' ,  is_update_time_exist )
    print ("------")
