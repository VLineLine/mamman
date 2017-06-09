import requests
import json
import pandas as pd

#reading configurations
with open('config.json') as conf_file:    
    conf = json.load(conf_file)

url='https://api.lts.no/api/v2/db-odoo1-lts/_table/project_task?related=project_category_by_project_category_project_task_rel%2C%09res_user_by_user_id'
headers ={'X-Dreamfactory-API-Key': conf['api-key-lts']}


#executing get command
resp = requests.get(url, headers=headers)

if resp.status_code != 200:
    # This means something went wrong
    print('ERROR, status-code == ' + str(resp.status_code))

data = resp.json()['resource']

for element in data:
    tags=""
    for categori_element in element['project_category_by_project_category_project_task_rel']:
        tags = tags + ', ' + categori_element['name']
    element['tags'] = tags.strip(', ')

pd.set_option('display.max_colwidth', -1)    
df = pd.DataFrame(data)


#Add column for year
df['year'] = df['create_date'].str[:4]

#Sort by create_date
df = df.sort_values('create_date', ascending=False)

#No need for create_date anymore
df = df.drop('create_date', 1)

#Remove rows without description
df = df[df['description'].notnull()]

#Changing place
df2 = df[['year', 'description', 'tags']]

#Changing column headers
df2.columns = ['År', 'Beskrivelse', 'Tag']

#Save file
df2.to_html('ref.htm',index=False, justify='left')
