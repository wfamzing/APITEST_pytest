import redis
import traceback

from common.read_file import ReadFile
from common.logger import Logger

class RedisOps:
    def __init__(self,conf):
        decrypt_password = conf['password'].encode()
        self.ip = conf["host"]
        self.port = int(conf["port"])
        self.password = decrypt_password
        self.db = int(conf["dbname"])
         #构造函数
        try:
            pool = redis.ConnectionPool(host=self.ip,port=self.port,password=self.password,db=self.db)
            self.r = redis.Redis(connection_pool=pool)
        except Exception as e:
            Logger.error(traceback.format_exc())

    def str_get(self,k):
        res = self.r.get(k)
        if res:
            return res.decode('utf-8')
        return None

    def str_get_incr(self, k):
        res = self.r.incr(k)
        if res:
            return res
        return None

    # 销毁对象时关闭数据库连接
    def __del__(self):
        try:
            self.r.connection_pool.disconnect()
        except Exception as e:
            Logger.error(traceback.format_exc())

    # 关闭数据库连接
    def close(self):
        self.__del__()

    def str_set(self,k,v,time=None):
        res=self.r.set(k,v,time)
        print('string数据插入成功')

    def str_delete(self,k):  #stt类型的删除key
        tag=self.r.exists(k)  #判断这个K是否存在5
        if tag:
            self.r.delete(k)
            print('数据删除成功')
        else:
            print('这个K不存在')

    def hash_get(self,name,k):   #hash类型获取单个key
        res=self.r.hget(name,k)
        if res:
            return res.decode()
        return None

    def hash_set(self,name,k,v):  #hash类型set
        self.r.hset(name,k,v)
        print('hash数据插入成功')

    def hash_getall(self,name):  #hash类型获取key里面的所有数据
        data={}
        res=self.r.hgetall(name)   #获取的数据类型是字典类型，要单个元素用decode()
        if res:
            for k,v in res.items():
                k=k.decode()
                v=v.decode()
                data[k]=v
            return data
        return None

    def hash_del(self,name,k):   #删除某个hash里面小key
        res=self.r.hdel(name,k)
        if res:
            print('小key删除成功')
            return 1
        else:
            print('删除失败，该K不存在')
            return 0

    def clean_redis(self):  #清理redis,删除所有的key
        self.r.flushdb() #清空redis
        print('清空redis成功')
        return 0



if __name__ == "__main__":
    redis_conf = ReadFile.get_config_dict()["redis"]["dev"]
    print(redis_conf)
    RedisOps = RedisOps(redis_conf)
    print(RedisOps.str_get("blade:auth::blade:captcha:72c59c7bdc750ec7d584eb31b5e80d0e"))
    # RO.hash_set('tanxxxxx_hash','tanrrrr','uiuiuiuii')
    # print('hash_getall:',RO.hash_getall('tantttt_hash'))