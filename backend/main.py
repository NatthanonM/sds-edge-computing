from flask import Flask, jsonify, request
from flask_cors import CORS
import central

app = Flask(__name__)
CORS(app)

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


@app.route("/get-location", methods=["POST"])
def get_location():
    request_data = request.get_json()
    input_query = request_data["finger_print"]
    building_ans = exthit.localize(input_query)
    ans = (inhit_dict[building_ans[0]]).localize(input_query)
    building_id = building_ans[0]
    floor, tag = ans["floor"], ans["tag"]
    res = {"building_id": building_id, "floor": floor, "tag": tag}
    return jsonify(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
