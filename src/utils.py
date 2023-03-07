import os, re

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import ffmpeg

def duration_to_seconds(duration):
    """Converts a YouTube video duration from ISO 8601 format to seconds."""
    match = re.match('PT(\d+H)?(\d+M)?(\d+S)?', duration).groups()
    hours = int(match[0][:-1]) if match[0] else 0
    minutes = int(match[1][:-1]) if match[1] else 0
    seconds = int(match[2][:-1]) if match[2] else 0
    return hours * 3600 + minutes * 60 + seconds

def get_meta(video_id, note_box_license):

    API_KEY = "AIzaSyCi-0otAqE59rywdfx0IdrMzP5niYWk_uo"

    # Set up the API client
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Get the video information
    try:
        video_info = youtube.videos().list(part='snippet,contentDetails,status', id=video_id).execute()
    except HttpError as e:
        print('An error occurred while getting video information:', e)
        exit()

    license_type = video_info['items'][0]['status']['license']
    conditions = {
        "Video is not processed to Youtube platform." : video_info['items'][0]['status']['uploadStatus'] != 'processed', 
        # "Video does not have a CreativeCommon license." : video_info['items'][0]['status']['license'] != 'creativeCommon',
        "Video has a licensed content in it." : video_info['items'][0]['contentDetails']['licensedContent'] == True
    }

    fails = []
    for key, value in conditions.items():
        if value:
            fails.append(f'{key}')

    be_aware = '\nBe aware to upload data not under Creative Commons or with stored licensed data in further projects.'
    
    if license_type=='creativeCommon':
        message = f"Video indeed has a CreativeCommon license. But it is not possible to directly determine if a video on YouTube has a public domain (CC0) or Attribute (CC-BY) type of license using the YouTube Data API v3. However, you can look for clues in the video's title or description, which may include information about the license. Many creators who use CreativeCommons will include information about the license in the title or description of their videos.\nIf video has BY (Attribution) right, it is necessary to give the author or licensor the credits (attribution) in the manner specified by these. "
        if len(fails) == 0:
            note_box_license.description = message
        else:
            note_box_license.description = message + "Also, video has following problems: " + (',').join(fails) + ' ' + be_aware
    
    elif license_type=='youtube':
        message = "Video has a standard YouTube license. Under the Standard YouTube License, viewers are allowed to watch the video on YouTube, share the video with others using YouTube's share features, and embed the video on other websites. However, any reproduction, modification, or distribution of the video outside of these terms is prohibited without the creator's explicit permission. "
        if len(fails) == 0:
            note_box_license.description = message
        else:
            note_box_license.description = message + "Also, video has following problems: " + (',').join(fails) + ' ' + be_aware
    
    else:
        raise RuntimeError('Unknown license type.')
    

    video_info_meta = {
        'duration_sec' : duration_to_seconds(
            video_info['items'][0]['contentDetails']['duration'] 
        ),
        'author' : video_info['items'][0]['snippet']['channelTitle'],
        'description' : video_info['items'][0]['snippet']['description'],
        'title' : video_info['items'][0]['snippet']['title'],
    }


    print(f'Received YouTube meta data is:\n{video_info_meta}')
    return video_info_meta


def get_youtube_id(link):

    assert link.startswith("https://www.youtube.com/"), "Invalid YouTube link. Please use desktop format of url starting with 'https://www.youtube.com/...'"
    try:
        # Extract the video ID from the link using regular expressions
        video_id = re.search(r'(?<=v=)[^&#]+', link).group(0)
    except AttributeError:
        # If the regular expression doesn't match, raise an exception with a custom error message
        raise ValueError("Invalid YouTube link.")
    
    print(f'Youtube ID is {video_id}')
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