from flask import Flask, abort, jsonify
import requests
import os
import central
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
example_query = central.init_example(example_id)
exthit = central.init_exthit(except_id=example_id)
inhit_dict = dict()
for b in example_building:
    inhit_dict[b] = central.init_inhit(b)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route("/central/<int:id>")
def hello_central(id):
    if id < 0 or id > len(example_id):
        abort(404, description="Not found")
    start = time.time()
    input_query = example_query[example_id[id]]
    building_ans = exthit.localize(input_query)
    ans = (inhit_dict[building_ans[0]]).localize(input_query)
    b, f = building_ans[0], ans
    end = time.time()
    return f"<p>Hello, Central!</p><p>{b} {f}</p><p>response time: {(end - start) * 1000} ms</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
