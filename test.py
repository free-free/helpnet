import tornadis
from tornado import gen,ioloop
from tornado_hbredis import TornadoHBRedis
from tornado_session import SessionCacheFactory
from storage  import StorageFactory
from config import Config
#client=tornadis.Client(host="localhost",port=6379,autoconnect=True)
#client=TornadoHBRedis('localhost',6379,True)
@gen.coroutine
def test_redis():
	sff=StorageFactory(Config.storage.all)
	st=sff.get_storage()
	#print(st.token())
	print(st.get_url("fhsuifesf.jpg"))
	#result=yield client.sadd("skey",[32,43,54,2])
	#print(result)
	#pipeline=client.pipeline()
	#pipeline.set("jj","huaangbiao")
	#pipeline.hmset("yyy",{"name":"huagbiao","age":21})
	#pipeline.lpush("zzz",[32,42,4,24,24,2])
	#pipeline.delete("yyy")
	#yield pipeline.execute()
	#result=yield client.call("hmset","test_hmset",*["sh1","key2","sh2","values"])
	#result=yield client.hkeys('test_hmset')
	#result=yield client.set("name","huangbiao")
	#result=yield client.mset({"age":21,"address":"SiChuan Province"})
	#result=yield client.mget(["age","name","address"])
	#result=yield client.sget("name")
	#result=yield client.exists("name")	
	#result=yield client.bitcount("name",0,1)
	#result=yield client.bit_or("age1","age0","xxx")
	#result=yield client.bit_and("age1","age0")
	#result=yield client.bit_xor("age1","age0")
	#result=yield client.bit_not("age0")
	#result=yield client.lpush("l1",["hello","world"])
	#result=yield client.rpush("l1",["lhello","lworld"])
	#result=yield client.lrange("l1",0,-1)
	#sessf=SessionCacheFactory('redis',"localhost",6379)
	#print(sessf.cache_size())
	#sess=sessf.get_session()
	#print(sessf.cache_size())
	#yield sess.start()
	#sess['name']='hangbiao'
	#yield sess.save()
	#sess.cache()
	#print(sessf.cache_size())
	#yield sess.start( "MGE1MWUzYzNlNzRkNDUxNjhjYmNkZWM5YzdlNmNhOWI=")
	#print(sess.all())
	#yield sess.destroy()
	#yield sess.start("YzJmOTEwOGQwNGIyNDg1OGIxMjljNDM5NDExY2YyZmM=")

	#yield sess.delete("name","YzJmOTEwOGQwNGIyNDg1OGIxMjljNDM5NDExY2YyZmM=")
	#yield sess.destroy("N2ZlNjllY2QzMzQwNDBhYmFhYzM2NDVkOGNkMDMyMmI=")
	#print(sess['name'])
	#print(sess['age'])
	#print(sess['address'])
	#print(sess.session_id)
	#yield sess.save()
	#yield sess.start()
	#sess['name']='xiaoming'
	#sess['age']=21
	#sess['address']='SiChuanProvince'
	#yield sess.start()
	#sess['name']='zhangshan'
	#sess['age']=22
	#sess['address']="BeiJing"
	#yield sess.save(15)
	
	#result=yield client.ldel("l1")
	#print(result)

loop=ioloop.IOLoop.current()
loop.run_sync(test_redis)
