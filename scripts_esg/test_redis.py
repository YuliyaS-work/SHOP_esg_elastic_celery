import os

from decouple import config
import redis

r = redis.Redis(host=config('REDIS_HOST'), port=config('REDIS_PORT'), db=config('REDIS_DB'))

r.set('yuliya', 'awesome')
print(r.get('yuliya'))

try:
    r.ping()
    print("Redis доступен!")
except redis.ConnectionError:
    print("Redis не отвечает.")
