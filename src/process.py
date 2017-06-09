import requests
import json
import base64

#reading configurations
with open('config.json') as conf_file:    
    conf = json.load(conf_file)
    conf_file.close()
url='https://api.lts.no/api/v2/db/_table/process'
headers ={'X-Dreamfactory-API-Key': conf['api-key-lts']}

def read_all():
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception('ERROR: API status code ' + str(resp.status_code))
    else:
        return(resp.json()['resource'])

def read_first():
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
            raise Exception('ERROR: API status code ' + str(resp.status_code))
    else:
        if len(resp.json()['resource']) == 0:
            raise Exception('no process in table')
        else:
            return(resp.json()['resource'][0])

if __name__ == "__main__":
    print(read_first())
