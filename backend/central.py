import os.path
from algorithm.exthit_bldg import ExtHit_Bldg
from algorithm.inhit import InHit
import json


def get_answer(id):
    # # data = []
    # # with open("Data/data.txt") as f:
    # #     for line in f:
    # #         data.append(json.loads(line))
    # # size = len(data)
    # # test_id = 1
    # # test_data = data[test_id]

    # selected_building = "ENG3"
    # data = []
    # with open(
    #     f"{os.path.dirname(__file__)}/../database/data/building-{selected_building}.txt"
    # ) as f:
    #     for line in f:
    #         data.append(json.loads(line))
    # size = len(data)
    # test_id = id
    # test_data = data[test_id]
    # train_data = data[:test_id] + data[test_id + 1 :]
    # inhit = InHit(100, 3, 100, data)
    # # ans = inhit.predict_all(test_data_list)
    # # start = time.time()
    # ans = inhit.localize(test_data["access_point"])
    # # end = time.time()
    # # print(ans)
    # # print((end - start) * 1000)
    # return ans

    data = []
    with open(f"{os.path.dirname(__file__)}/../database/data.txt") as f:
        for line in f:
            data.append(json.loads(line))
    test_id = id
    test_data = data[test_id]
    train_data = data
    exthit_bldg = ExtHit_Bldg(20, train_data[:test_id] + train_data[test_id + 1 :])

    building_ans = exthit_bldg.localize(test_data["access_point"])
    data = []
    with open(
        f"{os.path.dirname(__file__)}/../database/data/building-{building_ans[0]}.txt"
    ) as f:
        for line in f:
            data.append(json.loads(line))

    train_data = data
    inhit = InHit(100, 3, 100, train_data)
    ans = inhit.localize(test_data["access_point"])
    return building_ans[0], ans
