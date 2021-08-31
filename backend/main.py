from flask import Flask
import requests
import os
from central import get_answer
import time

app = Flask(__name__)


@app.route("/central/<int:id>")
def hello_central(id):
    start = time.time()
    b, f = get_answer(id)
    end = time.time()
    return f"<p>Hello, Central!</p><p>{b} {f}</p><p>response time: {(end - start) * 1000} ms</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
