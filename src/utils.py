import os, re

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import ffmpeg

def get_meta(video_id, checkbox_dict, note_box_license):

    API_KEY = "AIzaSyCi-0otAqE59rywdfx0IdrMzP5niYWk_uo"

    # Set up the API client
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Get the video information
    try:
        video_info = youtube.videos().list(part='snippet,contentDetails,status', id=video_id).execute()

        conditions = {
            "'uploadStatus' == 'processed'" : video_info['items'][0]['status']['uploadStatus'] == 'processed', 
            "'license' == 'creativeCommon'" : video_info['items'][0]['status']['license'] == 'creativeCommon',
            "'licensedContent' == 'False'" : video_info['items'][0]['contentDetails']['licensedContent'] == False
        }

        for key, value in conditions.items():
            if not value:
                # raise RuntimeError(f'License condition {key} failed. Be aware to upload licensed data in further projects.')
                note_box_license.description = f'License condition {key} failed. Be aware to upload data not under Creative Commons or with stored licensed data in further projects.'
        video_info_meta = {
            'author' : video_info['items'][0]['snippet']['channelTitle'],
            'description' : video_info['items'][0]['snippet']['description'],
            'title' : video_info['items'][0]['snippet']['title'],
        }
        
    except HttpError as e:
        print('An error occurred while getting video information:', e)
        exit()

    return {key: value for key, value in video_info_meta.items() if checkbox_dict[key]}

      

def get_youtube_id(link):

    assert link.startswith("https://www.youtube.com/"), "Invalid YouTube link"
    try:
        # Extract the video ID from the link using regular expressions
        video_id = re.search(r'(?<=v=)[^&#]+', link).group(0)
    except AttributeError:
        # If the regular expression doesn't match, raise an exception with a custom error message
        raise ValueError("Invalid YouTube link")
    return video_id
 

def trim(input_path, output_path, start:int=30, end:int=60):
    
    input_stream = ffmpeg.input(input_path)

    vid = (
        input_stream.video
        .trim(start=start, end=end)
        .setpts('PTS-STARTPTS')
    )
    aud = (
        input_stream.audio
        .filter_('atrim', start=start, end=end)
        .filter_('asetpts', 'PTS-STARTPTS')
    )

    joined = ffmpeg.concat(vid, aud, v=1, a=1).node
    output = ffmpeg.output(joined[0], joined[1], output_path)
    ffmpeg.run(output, overwrite_output=True)

    print('Video succesfully trimmed!')