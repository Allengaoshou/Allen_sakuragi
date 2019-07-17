#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
example：
redis_client = RedisClient()
redis_connect = redis_client.get_value("mylist", "LIST")
'''
from rediscluster import StrictRedisCluster
import RrdLogger
import socket
import redis
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

RUNNER_IP = '172.16.4.83'
class RedisClient():

    def __init__(self):
        self.logger = RrdLogger.RrdLogger().getLogger('redis client')
        # self.nodes = [{"host": '172.16.4.83', "port": i} for i in range(7000, 7006)]
        self.nodes = [{"host": '172.16.4.83', "port": 7000},
                      {"host": '172.16.4.83', "port": 7001},
                      {"host": '172.16.4.83', "port": 7002},
                      {"host": '172.16.4.83', "port": 7003},
                      {"host": '172.16.4.83', "port": 7004},
                      {"host": '172.16.4.83', "port": 7005}]
        self.key = None
        self.type_dict = {
            "STRING":{
                "DEL": self.__get_string
            },
            "STRING": {
                "GET": self.__get_string
            },
            "HASH": {
                "GET": self.__get_hash
            },
            "LIST": {
                "GET": self.__get_list
            }
        }

    def __redis_return_convert(self, return_value):
        '''
        把Json格式字符串解码转换成Python对象
        :param return_value: json串
        :return:
        '''
        try:
            value = json.loads(return_value)
        except:
            return return_value
        else:
            return value

    def connect_redis(self):
        '''
        判断是集群链接还是单点链接
        集群连接返回：连接对象
        单点连接返回：1
        :return: 连接对象 or 1
        '''
        #获取本机计算机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        self.logger.info("本机IP：{}".format(ip))

        if ip == RUNNER_IP:
            # 连接redis集群
            self.logger.info("******连接redis集群******")
            self.logger.info("redis集群node:{}".format(self.nodes))
            try:
                redis_conn = StrictRedisCluster(startup_nodes=self.nodes, decode_responses=True)
                return redis_conn
            except Exception as e:
                self.logger.info("redis集群链接失败：{}".format(e))
        else:
            # 单点连接
            self.logger.info("******单点连接redis******")
            return 1

    def delete(self,key):
        redis_conn = StrictRedisCluster(startup_nodes=self.nodes, decode_responses=True)
        redis_conn.delete(key)
        return self.type_dict[type]["DEL"](conn, name, key_name)

    def get_value(self, name, type, key_name = None):
        '''
        获取redis中数据
        单点连接才有循环查询redis数据
        集群连接直接获取redis数据
        :param name: 键值
        :param type: 数据类型
        :param key_name: 哈希表 name 中，给定域 key_name
        :return:
        '''
        con_resuelt = self.connect_redis()
        if con_resuelt == 1:
            # 单点连接redis来获取数据
            value = None
            for i, val in enumerate(self.nodes):
                try:
                    r = redis.StrictRedis(host=val['host'], port=val['port'], decode_responses=True)
                    value = self.get(r, name, type, str(val), key_name)
                    if value is not None:
                        return value,val['port']
                except Exception as e:
                    continue
            if value is None:
                self.logger.info("redis没有该数据或redis单点连接失败")
        else:
            # 集群方式获取redis数据
            return self.get(con_resuelt, name, type, str(self.nodes), key_name)

    def get(self, conn, name, type, redis_url, key_name):
        '''
        根据类型获取redis值
        :param conn: redis链接对象
        :param name: 键值
        :param type: 数据类型
        :param redis_url: redis地址
        :param key_name: 哈希表 name 中，给定域 key_name
        :return:
        '''
        self.logger.info("Requesting redis data(date type is {}): {} from Redis: {}".format(type, name, redis_url))
        return self.type_dict[type]["GET"](conn, name, key_name)

    def __get_string(self, conn, name, key_name):
        # 获取string类型值
        redis_return = conn.get(name)
        self.logger.info(self.__redis_return_convert(redis_return))
        return self.__redis_return_convert(redis_return)

    def __get_hash(self, conn, name, key_name):
        # 获取hush类型值
        if key_name is None:
            redis_return = conn.hgetall(name)
            self.logger.info("Get Hash All Item with Name {} return:".format(name))
            convert_result = self.__redis_return_convert(redis_return)
            if type(convert_result) == dict:
                for key in convert_result.keys():
                    convert_result[key] = self.__redis_return_convert(convert_result[key])
        else:
            if conn.hexists(name, key_name):
                redis_return = conn.hget(name, key_name)
            else:
                raise AttributeError("Hash Key {} is Not exist in {}".format(key_name, name))
            self.logger.info("Get Hash Key with Name {} Key {} return:".format(name, key_name))
            convert_result = self.__redis_return_convert(redis_return)
        self.logger.info(json.dumps(convert_result, sort_keys=True, indent=4, ensure_ascii=False))
        return convert_result


    def __get_list(self, conn, name, key_name):
        # 获取list类型值
        redis_return = conn.lrange(name, 0, -1)
        self.logger.info(self.__redis_return_convert(redis_return))
        return  redis_return


if __name__ =="__main__":
    redis_client = RedisClient()
    redis_connect5 = redis_client.get_value("P2P-REDIS_MOBILE_CODE_REGISTER_OR_LOGIN_18500461011", "STRING")


