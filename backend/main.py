from flask import Flask
import requests
import os
from edge import get_answer
import time

app = Flask(__name__)


@app.route("/<int:id>")
def hello_world(id):
    start = time.time()
    f = get_answer(id)
    end = time.time()
    return (
        f"<p>Hello, World!</p><p>{f}</p><p>response time: {(end - start) * 1000} ms</p>"
    )


@app.route("/central")
def hello_central():
    central_address = os.environ["central_address"]
    r = requests.get(central_address)
    print(r.status_code)
    return "<p>Hello, Central! {}</p>".format(central_address)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
