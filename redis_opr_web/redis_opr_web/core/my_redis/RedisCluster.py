import redis
from redis.exceptions import ResponseError
from .. import utils

from .RedisClient import Redis_client
# 普通方法返回值
from ...core.Common import CommonMethodResult
from . import RedisClient

# 通过一个节点获取整个集群得客户端连接
def getRedisClientListByOneNode(host , port , requirepass ):
	commonMethodResult = CommonMethodResult();
	one_node_redis_client = RedisClient.createRedisConn(host , port , requirepass);
	if one_node_redis_client.success:
		print(' 服务 ', host, ':', str(port), ' msg : ', one_node_redis_client.msg)
	else:
		commonMethodResult.success = False;
		msg = ' 服务 ' + host + ':' + str(port) + ' msg : ' + one_node_redis_client.msg;
		commonMethodResult.msg = msg;
		print(msg)
		return commonMethodResult;
	clusterNodes = getClusterNodes(one_node_redis_client);
	# 大于一个节点
	clientList = [];
	if clusterNodes and len(clusterNodes) > 1:
		for clusterNodesItem in clusterNodes :
			mHost = clusterNodesItem['host'];
			mPort = clusterNodesItem['port'];
			new_redis_client = RedisClient.createRedisConn(mHost, mPort, requirepass);
			clientList.append(new_redis_client);
	commonMethodResult.result = {};
	commonMethodResult.result['redis_client_list'] = clientList;
	commonMethodResult.success = True;
	return commonMethodResult;




# 是否支持集群
def isClusterEnabled(rs):
	clusterinfo = rs.redisClient.info('cluster');
	cluster_enabled = clusterinfo['cluster_enabled'];
	print('cluster_enabled : ' , cluster_enabled);
	if cluster_enabled == 1 :
		return True;
	else:
		return False;


# 移除节点 有槽位的节点不删除
def forget_node(nodes , forget_rs):
	if getNodeAssignedSlots(forget_rs) == None :
		forget_rs_node  = getClusterNodesOfMyself(forget_rs)
		forget_rs_node_id = forget_rs_node['node_id']
		for node_item in nodes:
			cluster_nodes = getClusterNodes(node_item);
			for cluster_node in cluster_nodes :
				if cluster_node['ismyself'] == False and forget_rs_node_id == cluster_node['node_id'] :
					res = node_item.redisClient.cluster('FORGET' ,forget_rs_node_id )
					if res == False :
						return False;
		forget_rs.redisClient.cluster('RESET');
		return True;
	else :
		print (' %s:%d forget fail because it has slots ' %( forget_rs.host ,forget_rs.port ))
		return None;



# 从节点
def replicate_node(slave_rs , master_rs):
	master_rs_node = getClusterNodesOfMyself(master_rs)
	master_rs_node_id = master_rs_node['node_id'];
	res = slave_rs.redisClient.cluster('REPLICATE' , master_rs_node_id);
	return res ;


def meet_node_to_cluster(from_rs , to_rs ):
	host = to_rs.host;
	port = to_rs.port;
	res = from_rs.redisClient.cluster('MEET' ,host , port );
	# print ( 'meet_node_to_cluster  host : %s , port :%d  , result : %s ' %(host , port , res ));
	return res;

#将节点都加入集群
def meet_nodes_to_cluster(nodes):
	if nodes and len(nodes) > 0 :
		if len(nodes) == 1:
			print ('只有一个节点')
			return None;
		node = nodes[0];
		if isClusterEnabled(node) :
			# 循环meet操作 ，防止集群同步问题
			for meet_node in nodes:
				meet_host = meet_node.host;
				meet_port = meet_node.port;
				# print ('meet_host : %s:%d  ' %( meet_host ,meet_port ))
				for to_meet_node in nodes:
					to_meet_host = to_meet_node.host;
					to_meet_port = to_meet_node.port;
					#不是同一个节点
					if meet_host == to_meet_host and to_meet_port == meet_port:
						continue
					else:
						# print ('to_meet_host %s:%d  ' %( to_meet_host ,to_meet_port ))
						if meet_node_to_cluster(meet_node , to_meet_node ) :
							continue;
						else :
							print (' %s:%d meet %s:%d fail ' %( meet_host ,meet_port ,to_meet_host ,to_meet_port ))
							return None;
		else:
			return None;


	print ('isNodesInCluster : ' , isNodesInCluster(nodes))
	return True;


# cluster info 命令的结果
def getClusterInfo(rs):
	clusterinfo = rs.redisClient.cluster('info');
	return clusterinfo;	

# 获取节点列表 role 0 全部 1 master 2 slave
def getClusterNodesInternal(redis_client , role  ):
	nodes = [];
	# redis_client = Redis_client(rs);

	clusternodes = redis_client.redisClient.cluster('nodes');
	for node in clusternodes :
		newNode = {};
		newNode['name'] = node;

		name = '';
		host = '';
		port = 0;
		name = node;
		atIndex = name.find('@');
		if  atIndex > -1 :
			name = node[0 : atIndex];
		maohaoIndex = name.find(':');
		if  maohaoIndex > -1 :
			names = name.split(':');
			host = names[0];
			port = names[1];

		# print ('host : %s port :%s  ' %( host ,str(port) ))
		newNode['host'] = host;
		newNode['port'] = port;

		newNode['value'] = clusternodes[node];
		value = clusternodes[node];
		newNode['node_id'] = value['node_id'];
		value = clusternodes[node];
		flags = value['flags'];
		ismyself = False;
		isSlave = False;
		if flags.find('slave') > -1 :
			isSlave = True;
		if flags.find('myself') > -1 :
			ismyself = True;
		newNode['ismyself'] = ismyself;
		newNode['isSlave'] = isSlave;

		if role == 0:
			nodes.append(newNode);
		elif role == 1 and isSlave == False:
			nodes.append(newNode);
		elif role == 2 and isSlave == True:
			nodes.append(newNode);
	return nodes;	

def getClusterNodes(rs ):
	return getClusterNodesInternal(rs , 0)


def getMasterClusterNodes(rs):
	return getClusterNodesInternal(rs , 1)

def getSlaveClusterNodes(rs):
	return getClusterNodesInternal(rs , 2)


# 获取节点自身的 node 信息
def getClusterNodesOfMyself(rs):
	clusternodes = rs.redisClient.cluster('nodes');
	for node in clusternodes :
		newNode = {};
		maohao_index = node.find(':');
		host = node[0 : maohao_index];
		port = node[maohao_index +1 : ];
		newNode['name'] = node;
		newNode['host'] = host;
		newNode['port'] = port;
		newNode['value'] = clusternodes[node];
		value = clusternodes[node];
		newNode['node_id'] = value['node_id'];
		flags = value['flags'];
		if flags.find('slave') > -1 :
			newNode['isSlave'] = True;
		else :
			newNode['isSlave'] = False;
		if flags.find('myself') > -1 :
			newNode['ismyself'] = True;
			return newNode;
	

# 槽位是否由该节点管理
def hasSlots(rs , slot_num):
	return hasSlotsFromTo(rs , slot_num , slot_num )


# 槽位是否由该节点管理
def hasSlotsFromTo(rs , from_slot_num , to_from_slot_num):
	if from_slot_num > to_from_slot_num :
		return False;
	node = getClusterNodesOfMyself(rs);
	node_id = node['node_id'];
	slots = getClusterSlots(rs);
	for slot in slots :
		node_id_item = slot['node_id'];
		if node_id_item == node_id :
			# 自身节点 
			# 在槽位范围中
			if slot['from_slots'] <= from_slot_num and to_from_slot_num <= slot['to_slots'] :
				return True;				
		else :
			continue;
	return False;


# 获取集群还未分配的槽位
def getClusterUnassignedSlots(rs):
	limitSlots = 16383;
	unassignedSlots = [];
	slots = getClusterSlots(rs);
	# print (' getClusterUnassignedSlots : ' , slots )
	if len(slots) == 0 :
		unassignedSlot = {
			'from_slots' : 0,
			'to_slots' : limitSlots
		}
		unassignedSlots.append(unassignedSlot);
	else :
		last_slot = 0;
		for i in range( 0 , len(slots)) :
			slot = slots[i];
			from_slots = slot['from_slots'];
			to_slots = slot['to_slots']
			new_from_slots = 0;
			new_to_slots = 0;
			unassignedSlot = {};
			# 判断第一个槽位是否从0 开始
			# print (' from_slots : ' , from_slots , ' to_slots : ' , to_slots );
			# print (' last_slot : ' , last_slot  );
			if i == 0 and from_slots != 0:
				new_from_slots = 0;
				new_to_slots = from_slots - 1;
			elif i == 0 and from_slots == 0:
				last_slot = to_slots;
				continue;
			# 最后一个区域是否覆盖 16383 区域的
			elif i == (len(slots) - 1) and to_slots != limitSlots:
				new_from_slots = last_slot + 1;
				new_to_slots = limitSlots;
			elif i == (len(slots) - 1) and to_slots == limitSlots:
				continue;
			else:
				if (from_slots - last_slot) == 1:
					last_slot = to_slots;
					continue
				new_from_slots = last_slot + 1;
				new_to_slots = from_slots - 1;
				# print (' new_from_slots : ' , new_from_slots , ' new_to_slots : ' , new_to_slots );

			# 下个循环的开始
			last_slot = to_slots;
			unassignedSlot['from_slots'] = new_from_slots;
			unassignedSlot['to_slots'] = new_to_slots;
			unassignedSlots.append(unassignedSlot);

	if len(unassignedSlots) > 0:
		return unassignedSlots;
	else :
		return None;



# 获取该节点被分配的槽位
def getNodeAssignedSlots(rs):
	assigned_slots = [];
	node = getClusterNodesOfMyself(rs);
	node_id = node['node_id'];
	slots = getClusterSlots(rs);
	for slot_item in slots :
		node_id_item = slot_item['node_id'];
		if node_id_item == node_id :
			# 自身节点
			# 在槽位范围中
			assigned_slots.append(slot_item);
	if len(assigned_slots) > 0 :
		return assigned_slots;
	else :
		return None;


# 获取集群分配的槽位
def getClusterSlots(rs):
	slots = [];
	clusterslots = rs.redisClient.cluster('SLOTS');
	for slotItemArr in clusterslots :
		slot = {
			'node_name' : '',
			'node_id' :'',
			'from_slots' : -1,
			'to_slots': 0,
			'host':'',
			'port': -1
		}

		for slotItem in slotItemArr :
			node_name = slot['node_name'];
			if isinstance(slotItem , list) :
				if node_name == '':
					# 主从节点会共同负责槽位所以会出现多个，只取第一个
					# print('数组类型')
					slot['node_name'] += slotItem[0]
					slot['host'] = slotItem[0]
					slot['node_name'] += ":"
					slot['node_name'] += str(slotItem[1])
					slot['port'] = slotItem[1]
					slot['node_id'] = slotItem[2]
				else:
					continue;
			else :
				# print('slots');
				if slot['from_slots'] == -1 :
					slot['from_slots'] = slotItem;
				else :
					slot['to_slots'] = slotItem;
		slots.append(slot);

	#排序
	#冒泡排序 按slots 大小排序
	for i in range( 0 , len(slots)):
		for j in range( 0 , len(slots) - 1 ):
			slotB = slots[j + 1];
			slotA = slots[j];
			if slotA['from_slots'] > slotB['from_slots'] :
				temp = slotB;
				slots[j + 1] = slotA;
				slots[j] = temp;
	return slots;





# 节点是否在同一集群
def isNodesInCluster(nodes):
	# 返回结果
	commonMethodResult = CommonMethodResult();
	clusternodes = None;

	# 循环比较
	for my_node in nodes:
		myClusterNodesArr = getClusterNodes(my_node);
		# 是否单节点
		myClusterHasMore = False;
		if myClusterNodesArr and len(myClusterNodesArr) > 1 :
			myClusterHasMore = True;

		# print('================================');
		# 单节点无需检测 可以随时被添加
		if not myClusterHasMore :
			continue;

		myClusterNodes = getClusterNodesOfMyself(my_node);
		my_node_id = myClusterNodes['node_id'];
		for nodeItem in nodes:
			if not (my_node.name == nodeItem.name) :
				# 获取集群对象
				nodeItemClusterNodesArr = getClusterNodes(nodeItem);
				if nodeItemClusterNodesArr:
					# 已经有1个节点以上的需要检测
					if len(nodeItemClusterNodesArr) > 1:
						existInNodes = False;
						for nodeItemClusterNodesItem in nodeItemClusterNodesArr :
							node_item_node_id = nodeItemClusterNodesItem['node_id'];
							if my_node_id == node_item_node_id :
								# print(' my_node_id : ' , my_node_id) ;
								# print(' my_node_name : ' , my_node.name) ;
								# print(' node_item_node_id : ' , node_item_node_id) ;
								# print(' nodeItem : ' , nodeItem.name) ;
								existInNodes = True;
								break;
						# 已经存在集群中
						if not existInNodes :
							commonMethodResult.success = False;
							msg = my_node.name + ' 实例  node_id : '+ my_node_id +' 与 '+ nodeItem.name + ' 实例 node_id : '+ node_item_node_id + ' 不在同一个集群中'
							print(msg)
							commonMethodResult.msg =  msg;
							return commonMethodResult;
					else:
						# 单个节点不需要检测， 可以随时添加
						continue
	commonMethodResult.success = True;
	msg = '检测成功 '
	print(msg);
	commonMethodResult.msg = msg;
	return  commonMethodResult;




# 平均分配 给新cluster 分配
def spareRandomSlotsToEmptyClusterNodes(nodes):
	clusernodes_result = isNodesInCluster(nodes)
	masterList = [];
	# 所有节点都在集群中
	if clusernodes_result.success :
		limitSlots = 16384
		# 选出master
		for node_item in nodes :
			cluster_node = getClusterNodesOfMyself(node_item);
			if cluster_node['isSlave'] == False :
				masterList.append(node_item);
		list_len = len(masterList);
		if list_len > 0 :
			rs = masterList[0];
			cluster_node = getClusterNodesOfMyself(rs);

			unassignedSlots = getClusterUnassignedSlots(rs);
			clusterinfo = getClusterInfo(rs);
			# 节点数量
			master_node_size = list_len;
			cluster_slots_assigned = clusterinfo['cluster_slots_assigned'];
			# 还未分配槽位
			if int(cluster_slots_assigned) == 0 :
				# 只有一个槽位
				if master_node_size == 1:
					from_slots = 0
					to_slots = 16383
					for sls in range(from_slots, to_slots + 1):
						addSlots(masterList[0] , sls);
				else:
					# 平均分配的槽位
					average_slots_to_add = int(limitSlots / master_node_size);
					assigned_slots_list = [];
					last_to_slots = 0;
					for i in range( 0 , master_node_size) :
						assigned_slots = {};
						if i == 0 :
							assigned_slots['from_slots'] = 0 ;
							assigned_slots['to_slots'] = average_slots_to_add;
							last_to_slots = assigned_slots['to_slots'];
						elif i == (master_node_size - 1):
							assigned_slots['from_slots'] = last_to_slots + 1 ;
							assigned_slots['to_slots'] = limitSlots - 1 ;
						else :
							assigned_slots['from_slots'] = last_to_slots + 1 ;
							assigned_slots['to_slots'] = last_to_slots + 1 + average_slots_to_add;
							last_to_slots = assigned_slots['to_slots'];
						assigned_slots_list.append(assigned_slots);

					for i in range( 0 , len(masterList)) :
						master_node = masterList[i];
						assigned_slots = assigned_slots_list[i];
						from_slots = assigned_slots['from_slots']
						to_slots = assigned_slots['to_slots']
						for sls in range(from_slots , to_slots + 1 ):
							addSlots(master_node , sls );
				return True;
			else :
				return '已经分配过'
		else :
			print ('无节点传入')
			return None;
	else:
		print ('不在集群中')
		return None;






def delSlots(from_rs ,slots ):
	# 先从原节点处删除
	delresult = from_rs.redisClient.cluster('delslots', slots);
	allResult = False;
	if delresult:
		allResult = True;
	result = getRedisClientListByOneNode(from_rs.host , from_rs.port , from_rs.pwd);
	if result.success :
		redis_client_list = result.result['redis_client_list'] ;
		for redis_client in redis_client_list :
			# 删除其他节点的槽位
			if not from_rs.name == redis_client.name :
				delresult = redis_client.redisClient.cluster('delslots', slots);
				if delresult:
					allResult = True;
		if not allResult :
			return False;
		else:
			return True;
	else:
		return result;


def addSlots(master_node_rs , slots):
	result = master_node_rs.redisClient.cluster('addslots' , slots);
	return result;



def addSlots(master_node_rs , slots):
	result = master_node_rs.redisClient.cluster('addslots' , slots);
	return result;


# CLUSTER SETSLOT slot IMPORTING|MIGRATING|STABLE|NODE [node_id]

def cluster_setslot_importing(taget_rs , slot , node_id):
	return cluster_setslot(taget_rs, "IMPORTING" , slot , node_id );

def cluster_setslot_migrating(taget_rs , slot  , node_id):
	return cluster_setslot(taget_rs , "MIGRATING" , slot  , node_id );

def cluster_setslot_stable(taget_rs , slot ):
	result = taget_rs.redisClient.cluster('SETSLOT' , slot , "STABLE" );
	return result;

# 通知节点 slot槽位由 node_id 管理
def cluster_setslot_node(taget_rs , slot , node_id):
	result = taget_rs.redisClient.cluster('SETSLOT' , slot , 'NODE'  , node_id);
	return result;

def cluster_setslot(taget_rs , cmd , slot , node_id ):
	result = taget_rs.redisClient.cluster('SETSLOT' , slot , cmd  , node_id);
	return result;

def clusterNode_getkeysinslot(rs , slot , count):
	result = rs.redisClient.cluster('getkeysinslot' , slot , count);
	return result;


# 迁移键到集群新节点 重新分片操作 from 节点 的 slot 迁移到 to 槽位
def migrate_slots_to_new_node( from_rs , to_rs , slot):
	# 返回结果
	result = {};
	result['msg'] = '操作成功';
	result['success'] = True;

	# 一次迁移的键个数
	migrate_count = 60;
	#判断两个节点是否同一个集群
	nodes = [];
	nodes.append(from_rs)
	nodes.append(to_rs)
	isInCluster = isNodesInCluster(nodes)
	if isInCluster.success :
		#同一集群
		clusterInfo = getClusterInfo(from_rs);
		#判断集群状态
		if clusterInfo['cluster_state'] == 'ok':
			# 状态ok
			# 判断slot 是否在from 节点
			has_slots = hasSlots(from_rs , slot);
			if has_slots :
				#存在
				# 迁移
				from_node = getClusterNodesOfMyself(from_rs);
				from_node_id = from_node['node_id'];
				to_node = getClusterNodesOfMyself(to_rs);
				# print ('to_node : ' , to_node);
				to_node_id = to_node['node_id'];
				# to节点通知 importing
				cluster_setslot_importing(to_rs , slot , from_node_id);
				# from 节点通知 migrating
				cluster_setslot_migrating(from_rs , slot , to_node_id);
				# 获取from 节点的keys
				to_migrate_keys = clusterNode_getkeysinslot(from_rs , slot ,migrate_count );
				to_host = to_node['host'];
				to_port = to_node['port'];
				# 获取旧密码
				to_node_requirepass = to_rs.redisClient.config_get('requirepass');
				#  格式是：{'requirepass': 'redis'} 后面重置回来时要 to_node_requirepass['requirepass']
				# print (' to_node_requirepass : ' , to_node_requirepass)
				while (to_migrate_keys != None and len(to_migrate_keys) > 0):
					# print (' to_migrate_keys : ' , to_migrate_keys)
					# print('len _ to_migrate_keys : ' , len(to_migrate_keys));
					# 将目标服务密码设置成取消 用于 migrate 服务 防止noauth 报错 操作时改密码，操作完马上改回来，防止出现安全问题
					try :
						set_requirepass_result = to_rs.redisClient.config_set('requirepass' , '');
						mig_result = cluster_migrate_keys_to_server(from_rs , to_host , to_port , *to_migrate_keys);
						# 密码改回来
					except ResponseError as e :
						exception = str(e);
						# 把状态变回
						cluster_setslot_stable(from_rs , slot  );
						cluster_setslot_stable(to_rs , slot  );
						print(' ResponseError : ' , exception);
						result['msg'] =  exception;
						result['success'] = False;
						return result;
					finally:
						reset_pass = to_rs.redisClient.config_set('requirepass' , to_node_requirepass['requirepass']);
						to_migrate_keys = clusterNode_getkeysinslot(from_rs , slot ,migrate_count );

				# print (' reset_pass : ', reset_pass , '  requirepass : ' , to_node_requirepass);
				# 通知
				setslot_node_result = cluster_setslot_node(to_rs , slot ,to_node_id );
				print ('重新分片成功 : ' , slot);
				return result;
			else :
				print ('from_rs 不存在槽位 : ' , slot);
				result['msg'] = 'from_rs 不存在槽位 : ' , slot;
				result['success'] = False;
				return result;



		else :
			print ('集群 cluster_state is not ok ')
			result['msg'] = '集群 cluster_state is not ok';
			result['success'] = False;
			return result;

	else :
		print ('节点不在同一集群 ')
		result['msg'] = '节点不在同一集群';
		result['success'] = False;
		return result;


#从节点 a 槽位范围转移到 b
def migrate_fromto_slots_to_new_node( from_rs , to_rs , from_slot , to_slot):
	result = {};
	result['msg'] = '操作成功';
	result['success'] = True;
	#判断槽位是否在里
	if hasSlotsFromTo(from_rs , from_slot , to_slot ) :
		for i in range(from_slot , to_slot + 1) :
			print ('转移槽位 : ' , i);
			#重新分片成功
			migrate_slots_result = migrate_slots_to_new_node(from_rs , to_rs  , i );
			if migrate_slots_result['success'] == True :
				# 成功
				continue
			else:
				return migrate_slots_result;
	else:
		result['msg'] = '槽位不在 from_rs 中';
		result['success'] = False;
		return result;






#键转移
# MIGRATE 192.168.1.34 6379 "" 0 5000 KEYS key1 key2 key3
def cluster_migrate_keys_to_node(node_rs , target_node_id , *keys  ):
	command_str = '';
	node = getClusterNodesOfMyself(node_rs);
	host = node['host'];
	port = node['port'];
	result = node_rs.redisClient.execute_command('MIGRATE' ,host , port , "" , 0 , 5000 , "keys" , *keys );
	return result;

# MIGRATE 192.168.1.34 6379 "" 0 5000 KEYS key1 key2 key3
def cluster_migrate_keys_to_server(node_rs , host , port , *keys  ):
	result = node_rs.redisClient.execute_command('MIGRATE' ,host , port , "" , 0 , 5000 , "keys" , *keys );
	return result;

# def migrateSlots(fromRs , toRs , fromSlot , toSlot):
# 	if fromSlot > toSlot :
# 		return False;
# 	for i in range(fromSlot ,toSlot ) :
# 		clusternodes = rs.redisClient.cluster('addslots' , );



# 根据 cluster slots 结果计算 slots 比例
def getSlotsCountInfo(redis_client , cluster_slots , host):
	if len(host) == 0:
		host = redis_client.host;

	cluster_slots_count = [];
	clusterInfo = getClusterInfo(redis_client);
	# assigned ok fail
	total = 16384;
	unassigned = total - int(clusterInfo['cluster_slots_assigned']);

	# 计算未分配的槽位区域
	unassignedSlotsInfo = '';
	unassignedSlotsStart = 16383;
	unassignedSlotsEnd = 0;
	unassignedSlotsLen = 0;
	if cluster_slots and len(cluster_slots) > 0 :
		# 理论上有  n + 1 段槽位未分配
		unassignedSlotsLen = len(cluster_slots) + 1;
		sorted_cluster_slots = cluster_slots;
		# 冒泡排序
		for i in range(len(sorted_cluster_slots) - 1):
			for j in range(len(sorted_cluster_slots) - i - 1):
				formerOne = sorted_cluster_slots[j];
				former_from_slots = formerOne['from_slots'];
				former_from_slots = int(former_from_slots)

				latterOne = sorted_cluster_slots[j + 1];
				latter_from_slots = latterOne['from_slots'];
				latter_from_slots = int(latter_from_slots)
				if former_from_slots > latter_from_slots :
					temp = latterOne;
					sorted_cluster_slots[j + 1] = formerOne;
					sorted_cluster_slots[j] = temp;

		# 计算未分配槽位
		if len(cluster_slots) > 1 :
			for i in range(len(cluster_slots) - 1):
				former_cluster_slot_item = cluster_slots[i];
				latter_cluster_slot_item = cluster_slots[i + 1];
				# 第一个节点
				former_to_slots = former_cluster_slot_item['to_slots'];
				former_from_slots = former_cluster_slot_item['from_slots'];
				latter_to_slots = latter_cluster_slot_item['to_slots'];
				latter_from_slots = latter_cluster_slot_item['from_slots'];

				former_to_slots = int(former_to_slots)
				former_from_slots = int(former_from_slots)
				latter_to_slots = int(latter_to_slots)
				latter_from_slots = int(latter_from_slots)


				# 开头
				if i == 0 :
					if former_from_slots > 0:
						unassignedSlotsStartFrom = 0;
						unassignedSlotsStartTo = former_from_slots - 1;
						unassignedSlotsInfo += str(unassignedSlotsStartFrom) + '-' + str(unassignedSlotsStartTo) + ' / ';


				unassignedSlotsStartFrom = former_to_slots + 1;
				unassignedSlotsStartTo = latter_from_slots - 1;
				unassignedSlotsInfo += str(unassignedSlotsStartFrom) + '-' + str(unassignedSlotsStartTo) + ' / ';

				# 结尾
				if i == (len(cluster_slots) - 2 ) :
					if latter_to_slots < 16383:
						unassignedSlotsStartFrom = latter_to_slots + 1;
						unassignedSlotsStartTo = 16383;
						unassignedSlotsInfo += str(unassignedSlotsStartFrom) + '-' + str(
							unassignedSlotsStartTo) + ' / ';
			if len(unassignedSlotsInfo) > 0:
				unassignedSlotsInfo = unassignedSlotsInfo[0 : len(unassignedSlotsInfo) - 2]


		for cluster_slot_item in cluster_slots:
			nodeId = cluster_slot_item['node_id'];
			name = cluster_slot_item['node_name'];
			nameArr = name.split(':');
			# 自己一个的集群
			if len(nameArr[0]) == 0:
				name =  host + name;

			name = name.replace('127.0.0.1' , host);
			# 已经计算过节点
			slot_count = 0;
			to_slots = cluster_slot_item['to_slots'];
			from_slots = cluster_slot_item['from_slots'];
			to_slots = int(to_slots)
			from_slots = int(from_slots)

			slot_dis = 0;
			if from_slots == to_slots :
				slot_dis = 1;
			else:
				slot_dis = cluster_slot_item['to_slots'] - cluster_slot_item['from_slots'] + 1;

			new_slot_count_item = {};
			containsSlots = False;
			# 已经存在就不在再插入
			slotsInfo = str(from_slots) + '-' + str(to_slots);
			for slot_count_item in cluster_slots_count:
				if slot_count_item['nodeId'] == nodeId :
					containsSlots = True;
					old_slot_count = slot_count_item['slot_count'];
					slot_count = old_slot_count + slot_dis;
					slotsInfo = slot_count_item['slotsInfo'] + ' | ' + slotsInfo;
					slot_count_item['slotsInfo'] = slotsInfo;
					slot_count_item['slot_count'] = slot_count;

			if not containsSlots :
				slot_count = slot_dis;
				new_slot_count_item['nodeId'] = nodeId;
				new_slot_count_item['slotsInfo'] = slotsInfo;
				new_slot_count_item['slot_count'] = slot_count;
				new_slot_count_item['nodeName'] = name;
				cluster_slots_count.append(new_slot_count_item);


	new_slot_count_item = {};
	new_slot_count_item['nodeId'] = '';
	new_slot_count_item['slot_count'] = unassigned;
	new_slot_count_item['nodeName'] = 'unassigned';
	new_slot_count_item['slotsInfo'] = unassignedSlotsInfo;
	cluster_slots_count.append(new_slot_count_item);


	new_fail_item = {};
	new_fail_item['nodeId'] = '';
	new_fail_item['slot_count'] = clusterInfo['cluster_slots_fail'];
	new_fail_item['nodeName'] = 'fail';
	new_fail_item['slotsInfo'] = '';
	cluster_slots_count.append(new_fail_item);

	return cluster_slots_count;


