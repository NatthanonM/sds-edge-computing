from flask import Flask, abort, jsonify, request
import requests
import os
import edge
import time

app = Flask(__name__)

CENTRAL_ADDRESS = "http://localhost:5000"
SELECT_BUILDING = "POL3"

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
inhit = edge.init_inhit(SELECT_BUILDING)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route("/get-location", methods=["POST"])
def get_location():
    request_data = request.get_json()
    input_query = request_data["finger_print"]
    global SELECT_BUILDING, CENTRAL_ADDRESS
    if request_data["building_id"] == SELECT_BUILDING:
        ans = inhit.localize(input_query)
        floor, tag = ans["floor"], ans["tag"]
        res = {"building_id": SELECT_BUILDING, "floor": floor, "tag": tag}
    else:
        central_url = f"{CENTRAL_ADDRESS}/get-location"
        r = requests.post(central_url, json={"finger_print": input_query})
        building_id, floor, tag = (
            r.json()["building_id"],
            r.json()["floor"],
            r.json()["tag"],
        )
        res = {"building_id": building_id, "floor": floor, "tag": tag}
    return jsonify(res)


@app.route("/<int:id>")
def hello_world(id):
    if id < 0 or id > len(example_id):
        abort(404, description="Not found")
    start = time.time()
    input_query = example_query[example_id[id]]
    ans = (inhit_dict[example_building[id]]).localize(input_query)
    end = time.time()
    return f"<p>Hello, Edge!</p><p>{example_building[id]} {ans}</p><p>response time: {(end - start) * 1000} ms</p>"


@app.route("/central/<int:id>")
def hello_central(id):
    if id < 0 or id > len(example_id):
        abort(404, description="Not found")
    start = time.time()
    central_address = f"http://54.179.136.231:5000/central/{id}"
    r = requests.get(central_address)
    building_id, location = r.json()["building_id"], r.json()["location"]
    end = time.time()
    return f"<p>Hello, Central!</p><p>{building_id} {location}</p><p>response time: {(end - start) * 1000} ms</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
