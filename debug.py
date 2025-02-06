import json

# write a random json
# with open('debug.json', 'w') as f:
#     json.dump({'a': 1, 'b': 2}, f)

# read the json
with open('./mad_demo/src/assets/demo_metadata.json', 'r') as f:
    data = json.load(f)
    print(data[9].keys())
    