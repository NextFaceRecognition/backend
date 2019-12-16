import json

# Read parameter file
with open('service/parameters.json', 'r') as f:
    parameters = json.load(f)
# Tolerance is equals to 1 - similarity threshold
parameters['tolerance'] = 1 - float(parameters['sim_threshold'])