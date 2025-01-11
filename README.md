# Strava Corrector

This project connects to the Strava API to retrieve previous activities and reupload them with corrected data.

## Context

I used to run with an Apple Watch to record my runs. When I switched to another watch, I noticed that my previous watch 
had incorrect data (overestimating distance, making my statistics wrong). However, I discovered that the GPX file was 
accurate and that I could extract the correct distance and time from it. By downloading the GPX file and reuploading it 
to Strava, the activity is corrected.

To correct all my previous runs (more than 100 runs), I decided to write a quick script that would automate this process 
for me.

## Features

- Connects to the Strava API
- Retrieves previous activities
- Downloads GPX files
- Extracts correct distance and time from GPX files
- Reuploads corrected activities to Strava with same metadata
