import json

# write a random json
with open('debug.json', 'w') as f:
    json.dump({'a': 1, 'b': 2}, f)