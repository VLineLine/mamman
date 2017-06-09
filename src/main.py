import requests
import json

#reading configurations
with open('config.json') as conf_file:    
    conf = json.load(conf_file)

url='https://api.lts.no/api/v2/db/_table/task' # read all tasks
headers ={'X-Dreamfactory-API-Key': conf['api-key-lts']}


#executing get command
resp = requests.get(url, headers=headers)

if resp.status_code != 200:
    # This means something went wrong
    print('ERROR, status-code == ' + str(resp.status_code))

data = resp.json()['resource']

print(data)
