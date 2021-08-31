import json

data = []
with open('data.txt') as f:
    for line in f:
        data.append(json.loads(line))
buildings = {}
for sc in data:
    if sc["building_id"] not in buildings:
        buildings[sc["building_id"]] = [sc]
    else:
        buildings[sc["building_id"]].append(sc)
sumn = 0
for building_id in buildings.keys():
    with open('data/building-{}.txt'.format(building_id), 'w') as f:
        for t in buildings[building_id]:
          json.dump(t, f)
          f.write('\n')
              
    sumn += len(buildings[building_id])
    print(building_id, len(buildings[building_id]))
print('Total', sumn)
