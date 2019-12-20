from flask import Flask
from redis import Redis, RedisError
import os
import socket
import json

# Connect to Redis
try:
    VCAP_SERVICES = json.loads(os.environ["VCAP_SERVICES"])
    CREDENTIALS = VCAP_SERVICES["rediscloud"][0]["credentials"]
    redis = Redis(
        host=CREDENTIALS["hostname"],
        port=CREDENTIALS["port"],
        password=CREDENTIALS["password"],
        db=0,
        socket_connect_timeout=2,
        socket_timeout=2,
    )

except Exception:
    redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)


@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>Cannot connect to Redis, counter disabled</i>"

    html = """
        <h3>Hello World!</h3>
        <p>Here I am having fun with Pivotal Web Service!!</p>
        <p><strong>Visits:</strong> {visits}</p>
        <p>Request served by server: {hostname}</p>
        """.format(
        visits=visits, hostname=socket.gethostname()
    )

    return html


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
