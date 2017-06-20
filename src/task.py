import requests
import json
import base64

#setting up variables
with open('conf\config.json') as conf_file:    
    conf = json.load(conf_file)
    conf_file.close()
url='https://api.lts.no/api/v2/db/_table/task'
headers ={'api-key': conf['api-key-lts']}

def read_all():
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception('ERROR: API status code ' + str(resp.status_code))
    else:
        return(resp.json()['resource'])

def read():
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
            raise Exception('ERROR: API status code ' + str(resp.status_code))
    else:
        if len(resp.json()["resource"]) == 0:
            raise Exception('no task in table')
        else:
            return(resp.json()['resource'][0])

def post(data):
    resp = requests.post(url=url, data=json.dumps({'resource': [data]}), headers=headers) 
    if resp.status_code != 200:
        raise Exception('ERROR: API status code ' + str(resp.status_code))
    else:
        return(resp.json()['resource'][0]['id'])

if __name__ == "__main__":
    import process, pprint
    var = process.read_first() #reading one process
    pprint.pprint(var)
    process_id = var.pop('id') #popping ID
    var.update({'process_id': process_id }) #adding process ID
    print(post(var)) #testing POST feature
