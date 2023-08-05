import os


def has_redis_server():
    with os.popen("redis-server --version") as output:
        return bool(output.read())
