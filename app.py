from flask import Flask
from redis import Redis, RedisError
import os
import re
import socket

# Detect service name
for k in dict(os.environ).keys():
    if re.match(".*_SERVICE_HOST", k) and not re.match(
        "(KUBERNETES|REDIS)_SERVICE_HOST", k
    ):
        SERVICE_NAME = re.sub("_SERVICE_HOST$", "", k)

# Connect to Redis
redis = Redis(
    host=os.getenv("REDIS_SERVICE_HOST", "redis"),
    port=os.getenv("REDIS_SERVICE_PORT", 6379),
    password=os.getenv("database-password"),
    db=0,
    socket_connect_timeout=2,
    socket_timeout=2,
)

app = Flask(__name__)


@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>Cannot connect to Redis, counter disabled</i>"

    html = """
        <h3>Hello World!</h3>
        <p>Here I am having fun with OpenShift!!</p>
        <p><strong>Visits:</strong> {visits}</p>
        <p>Request served by server: {hostname}</p>
        """.format(
        visits=visits, hostname=socket.gethostname()
    )

    return html


if __name__ == "__main__":
    app.run(
        debug=False,
        host="0.0.0.0",
        port=int(os.getenv(SERVICE_NAME + "_SERVICE_PORT", "5000")),
    )
