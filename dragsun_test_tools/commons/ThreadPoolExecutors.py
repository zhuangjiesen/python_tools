'''
多线程工具

'''
import threadpool


THREAD_SIZE = 5;

pool = threadpool.ThreadPool(THREAD_SIZE)
requests = threadpool.makeRequests(scheduledGetRedisInfo, task_list)
[pool.putRequest(req) for req in requests]
pool.wait()




