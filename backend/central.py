import os.path
from algorithm.exthit_bldg import ExtHit_Bldg
from algorithm.inhit import InHit
import json
from typing import List, Dict, Any


def init_example(id_list: List[int] = []) -> Dict[int, Any]:
    data = []
    with open(f"{os.path.dirname(__file__)}/../database/data.txt") as f:
        for line in f:
            data.append(json.loads(line))
    example_dict = dict()
    for id in id_list:
        example_dict[id] = data[id]["access_point"]
    return example_dict


def init_exthit(except_id: List[int] = []) -> ExtHit_Bldg:
    data = []
    with open(f"{os.path.dirname(__file__)}/../database/data.txt") as f:
        for line in f:
            data.append(json.loads(line))
    for e in except_id:
        del data[e]
    exthit_bldg = ExtHit_Bldg(20, data)
    return exthit_bldg


def init_inhit(building_name: str) -> InHit:
    data = []
    with open(
        f"{os.path.dirname(__file__)}/../database/data/building-{building_name}.txt"
    ) as f:
        for line in f:
            data.append(json.loads(line))
    inhit = InHit(100, 3, 100, data)
    return inhit


def get_answer(
    exthit_obj: ExtHit_Bldg, inhit_obj: InHit, access_point: List[Dict[str, Any]]
) -> Dict[str, Any]:
    building_ans = exthit_obj.localize(access_point)
    inhit_ans = inhit_obj.localize(access_point)
    ans_dict = {
        "building": building_ans[0],
        "floor": inhit_ans["floor"],
        "tag": inhit_ans["tag"],
    }
    return ans_dict
