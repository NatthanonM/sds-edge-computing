import os.path
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


def init_inhit(building_name: str) -> InHit:
    data = []
    with open(
        f"{os.path.dirname(__file__)}/../database/data/building-{building_name}.txt"
    ) as f:
        for line in f:
            data.append(json.loads(line))
    inhit = InHit(100, 3, 100, data)
    return inhit
