# %%
import json

# %%
''' unloading json file '''
with open('afk_list.json', 'r') as a_file:
    json_obj = json.load(a_file)

# %%
''' ADDING keys and values
if statement stops it from replacing keys and values '''

if 'server 1' in json_obj:
    json_obj['server 1' ].update({'user 3': {"name before": "George","afk message": "running"}})
else:
    json_obj.update({'server 1': {'user 3': {"name before": "George","afk message": "running"}}})
print(json.dumps(json_obj, indent=4))


# %%
''' REMOVING keys and values '''
if 'user 3' in json_obj['server 1']:
    del json_obj['server 1']['user 3']

# %%
''' loading json file '''
with open('afk_list.json', 'w') as a_file:
    json.dump(json_obj, a_file, indent=4, ensure_ascii=False)

