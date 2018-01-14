# redis 集群操作

import redis
  
#链接redis数据库  
from redis_tools import RedisClient
from redis_tools import RedisCluster


# redis 客户端对象：
# redis['redis'] redis连接
# redis['host'] host
# redis['port'] 端口号



# decode_responses 一定要加 否则cluster 命令获取结果报错  password = 'redis' ,
rs6579 = {};

rs6579 = RedisClient.createRedisConn('192.168.130.130' , 6579 , None);
rs6580 = RedisClient.createRedisConn('192.168.130.130' , 6580 , None);
rs6581 = RedisClient.createRedisConn('192.168.130.130' , 6581 , None);
# rs6582 = AppRedis.createRedisConn('192.168.130.130' , 6582 , None);
# rs6679 = AppRedis.createRedisConn('192.168.130.130' , 6679 , None);



# 判断服务是否集群
isClusterEnabled = RedisCluster.isClusterEnabled(rs6579);
if isClusterEnabled :
	print('集群模式')
else : 
	print('非集群模式')
# 获取 cluster info 结果
clusterinfo = RedisCluster.getClusterInfo(rs6579);
print('clusterinfo : ' , clusterinfo);

clusternodes = RedisCluster.getClusterNodes(rs6579);
print('clusternodes : ' , clusternodes);


# clusternodes = rs6579.cluster('nodes');
# for node in clusternodes:
# 	print('node : ' , node);

# slots = Redis_Cluster.getClusterSlots(rs6579);
# print(' slots : ' , slots);
# print(' rs6580 hasSlotsFromTo : ' , Redis_Cluster.hasSlotsFromTo(rs6580 , 10050 , 11000 ))
# print(' rs6580 has 10050 : ' , Redis_Cluster.hasSlots(rs6580 , 10050 ))
# print(' rs6580 has 3 : ' , Redis_Cluster.hasSlots(rs6580 ,  3 ))
# print(' rs6579 has 15000 : ' , Redis_Cluster.hasSlots(rs6579 , 15000 ))
# print(' rs6579 has 3000 : ' , Redis_Cluster.hasSlots(rs6579 , 3000 ))
# unassignedSlots = Redis_Cluster.getClusterUnassignedSlots(rs6579);
# print(' unassignedSlots : ' , unassignedSlots);


meet_nodes = [];
meet_nodes.append(rs6579);
meet_nodes.append(rs6580);
meet_nodes.append(rs6581);
# meet_nodes.append(rs6582);
# meet_nodes.append(rs6679);


#全都加入集群
# res_meet = RedisCluster.meet_nodes_to_cluster(meet_nodes)
# print (' meet nodes ..... : ' , res_meet);

slot_nodes = [];
slot_nodes.append(rs6579);
slot_nodes.append(rs6580);
slot_nodes.append(rs6581);
# slot_nodes.append(rs6582);
# slot_nodes.append(rs6679);
#分配槽位 平均
spareResult = RedisCluster.spareRandomSlotsToEmptyClusterNodes(slot_nodes)
print('spareResult : ' , spareResult)

#设置从节点
# res_replicate_node = Redis_Cluster.replicate_node(rs6582 , rs6580);
# print ('res_replicate_node : ' , res_replicate_node);
# res_replicate_node_2 = Redis_Cluster.replicate_node(rs6679 , rs6580);


# print ('res_replicate_node_2 : ' , res_replicate_node_2);


# forget_res = Redis_Cluster.forget_node(meet_nodes ,rs6679 );
#移除节点
# for forget_node in meet_nodes:
# 	forget_res = Redis_Cluster.forget_node(meet_nodes ,forget_node );
# 	print ('移除节点 host : %s , port : %d  result : %s : ' %(forget_node['host'],forget_node['port'],forget_res));





# assignedSlots = Redis_Cluster.getNodeAssignedSlots(rs6579);
# print('assignedSlots : ' , assignedSlots)

# clusterSlots = Redis_Cluster.getClusterSlots(rs6579);
# print('getClusterSlots : ' , clusterSlots)

# unassignedSlots = Redis_Cluster.getClusterUnassignedSlots(rs6579);
# print('unassignedSlots : ' , unassignedSlots)






# isNodesInCluster = Redis_Cluster.isNodesInCluster(nodes)
# print('isNodesInCluster : ' , isNodesInCluster)


# keysinslot = Redis_Cluster.clusterNode_getkeysinslot(rs6580 , 4000 ,10);
# print ('keysinslot : ' , keysinslot);
# # 重新分片成功
# migrate_slots_result = Redis_Cluster.migrate_slots_to_new_node(rs6579 ,rs6581 , 11000 );
# print ('migrate_slots_result : ' , migrate_slots_result);


# keys = [];
# keys.append('key:000050472471');
# migrate_keys_result = Redis_Cluster.cluster_migrate_keys_to_server(rs6579 , '192.168.130.130' ,6379 , *keys );
# print ('migrate_keys_result : ' , migrate_keys_result);

# for i in range(10000 , 12000):
# 	rs6580.cluster('addslots' , i);


# for i in range(1000 , 2000):
	# rs6579.cluster('addslots' , i);



#槽转移
# assignedSlots = Redis_Cluster.getNodeAssignedSlots(rs6581);
# print('assignedSlots : ' , assignedSlots)
# for slot in assignedSlots :
# 	from_slots = slot['from_slots']
# 	to_slots = slot['to_slots']
# 	migrate_slots_result = Redis_Cluster.migrate_fromto_slots_to_new_node(rs6581 , rs6582  , from_slots , to_slots);
# 	if migrate_slots_result['success'] :
# 		print ('转移成功')
# 	else :
# 		print ('转移失败')




