
from redis import Redis, RedisError
import os
import socket

# Connect to Redis
redis = Redis(host="34.204.188.22",port=6379, db=0, socket_connect_timeout=2, socket_timeout=2)

def hello():
    try:
        print('Start')
        visits = redis.incr("counter")
        print(visits)
    except RedisError as e:

        print(str(e))

if __name__ == "__main__":
    hello()
