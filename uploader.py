import csv
import os

import pandas as pd
import requests

from auth2 import access_token

url = "https://www.strava.com/api/v3/uploads"
header = {'Authorization': 'Bearer ' + access_token}

def upload(id, name, desc):
    url = "https://www.strava.com/api/v3/uploads"
    header = {'Authorization': 'Bearer ' + access_token}

    params = {'data_type': 'gpx', 'name': name, 'commute': 'false', 'description': desc, 'sport_type': 'Run'}
    files = {
        'file': open(f'gpx_files/{id}.gpx', 'rb')
    }
    res = requests.post(url, headers=header, params=params, files=files)
    return res

activities = pd.read_csv('activities.csv')

uploaded_activities = []

# Upload gpx files
for file in os.listdir('gpx_files'):
    if file.endswith(".gpx"):
        id = file.split(".")[0]
        name = activities[activities['id'] == int(id)]['name'].values[0]
        desc = ("Reuploading with correct GPS data from gpx file")
        res = upload(id, name, desc)
        res = res.json()
        print(file + " : " + str(res))
        uploaded_activities.append([id, res['id'], res['error'], res['status']])
        if res['error']:
            break

# Write uploaded activities to csv file
with open('uploaded_activities.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'upload_id', 'error', 'status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for activity in uploaded_activities:
        writer.writerow(
            {'id': id, 'upload_id': res['id'], 'error': res['error'], 'status': res['status']})

