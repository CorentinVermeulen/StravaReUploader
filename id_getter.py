"""
Project to correct my strava activities.
I used to record all my activities with an apple watch but the GPS was not working well.
I need to download the gpx file associated with the activity, delete the activity from strava and upload it again.
This project will do it for me.
"""
import requests
from auth2 import access_token
from datetime import datetime, timedelta
import csv


# Get all activities IDs for running activities

page = 1  # 1 to 2

header = {'Authorization': 'Bearer ' + access_token}

# Get all activities
activites_url = "https://www.strava.com/api/v3/athlete/activities"
request_page_num = 1
data = []
while True:
    param = {'per_page': 200, 'page': request_page_num}
    request_data = requests.get(activites_url, headers=header, params=param).json()

    if len(request_data) == 0:
        print("Total data length: %s" % len(data))
        print("No more data to request\n")
        break
    else:
        if request_data:
            data += request_data
            request_page_num += 1

# Prepare the data

## Keep only RUN activities and before 01/09/2023
activities = []
date_limit = datetime.strptime("2023-09-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ").date()
for activity in data:
    activity_date = datetime.strptime(activity["start_date_local"], "%Y-%m-%dT%H:%M:%SZ").date()
    if (activity["type"] == "Run") and (activity_date < date_limit):
        activities.append(activity)

print("Total 'Run' activities: %s\n" % len(activities))

# Print to csv file activity id, name and start date local
with open('activities.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'name', 'start_date_local', 'start_latlng']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for activity in activities:
        writer.writerow({'id': activity['id'], 'name': activity['name'], 'start_date_local': activity['start_date_local'], 'start_latlng': activity['start_latlng']})

print("File 'activities.csv' created\n")