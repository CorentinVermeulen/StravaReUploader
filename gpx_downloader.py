import requests
from auth2 import access_token
import pandas as pd
from datetime import datetime, timedelta
import gpxpy
import os
import time

# Download gpx file for an activity
def download_gpx(id, start_time, file_path):

    url = f"https://www.strava.com/api/v3/activities/{id}/streams"
    header = {'Authorization': 'Bearer ' + access_token}

    latlong = requests.get(url, headers=header, params={'keys': ['latlng']}).json()
    time_list = requests.get(url, headers=header, params={'keys': ['time']}).json()
    altitude = requests.get(url, headers=header, params={'keys': ['altitude']}).json()

    for r in [latlong, time_list, altitude]:
        if isinstance(r, dict) and 'message' in r.keys():
            check = r['message']
            if check == 'Rate Limit Exceeded':
                #exit('Rate Limit Exceeded, restart in 15 mins')
                print('Rate Limit Exceeded, restart in 15 mins')
                return False
            else:
                print(check)
                return False

    latlong = latlong[0]['data']
    time_list = time_list[1]['data']
    altitude = altitude[1]['data']

    data = pd.DataFrame([*latlong], columns=['lat', 'long'])
    data['altitude'] = altitude
    start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
    data['time'] = [(start_time + timedelta(seconds=t))
                    for t in time_list]

    gpx = gpxpy.gpx.GPX()
    # Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    # Create first segment in our GPX track:
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # Create points:
    for idx in data.index:
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(
            data.loc[idx, 'lat'], data.loc[idx, 'long'], elevation=data.loc[idx, 'altitude'], time=data.loc[idx, 'time']))

    with open(file_path, 'w') as f:
        f.write(gpx.to_xml())
    return True


# Read activities.csv
activities = pd.read_csv('activities.csv')

# Loop over activities
data_folder = "gpx_files"
for idx in activities.index:
    id = activities.loc[idx, 'id']
    start_time = activities.loc[idx, 'start_date_local']

    file_name = f"{data_folder}/{id}.gpx"

    if len(activities.loc[idx, 'start_latlng'].split(',')) != 2:
        print(f'Skipping activity, no GPS: {id}')

    elif f"{id}.gpx" in os.listdir(data_folder):
        print(f'Skipping activity, already downloaded: {id}')

    else:
        res = download_gpx(id, start_time, file_name)
        print("\rDownloaded %s files" % (idx+1) , '\r', end='')

        if not res:
            for i in range(15):
                print("\rWaiting %s minutes" % (15-i), '\r', end='')
                time.sleep(60)