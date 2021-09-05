from flask import Flask, abort, jsonify
import requests
import os
import edge
import time

app = Flask(__name__)

example_id = [1, 71, 167, 188, 202, 235, 269, 294, 303, 336]
example_building = [
    "POL3",
    "ARCH",
    "ENG4",
    "EN100",
    "ENG2",
    "ENG1",
    "MCS",
    "MHVH",
    "MHMK",
    "PHYS1",
]
example_query = edge.init_example(example_id)
inhit_dict = dict()
for b in example_building:
    inhit_dict[b] = edge.init_inhit(b)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route("/<int:id>")
def hello_world(id):
    if id < 0 or id > len(example_id):
        abort(404, description="Not found")
    start = time.time()
    input_query = example_query[example_id[id]]
    ans = (inhit_dict[example_building[id]]).localize(input_query)
    end = time.time()
    return f"<p>Hello, Edge!</p><p>{example_building[id]} {ans}</p><p>response time: {(end - start) * 1000} ms</p>"


@app.route("/central")
def hello_central():
    central_address = os.environ["central_address"]
    r = requests.get(central_address)
    print(r.status_code)
    return "<p>Hello, Central! {}</p>".format(central_address)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
