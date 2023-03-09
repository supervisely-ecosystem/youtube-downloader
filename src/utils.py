import os, re
# import supervisely as sly
import src.globals as g

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import ffmpeg


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

def duration_to_seconds(duration):
    """Converts a YouTube video duration from ISO 8601 format to seconds."""
    match = re.match('PT(\d+H)?(\d+M)?(\d+S)?', duration).groups()
    hours = int(match[0][:-1]) if match[0] else 0
    minutes = int(match[1][:-1]) if match[1] else 0
    seconds = int(match[2][:-1]) if match[2] else 0
    return hours * 3600 + minutes * 60 + seconds

def get_meta(video_id, note_box_license_1, note_box_license_2):

    # Set up the API client
    youtube = build('youtube', 'v3', developerKey=g.YT_API_KEY)

    # Get the video information
    try:
        video_info = youtube.videos().list(part='snippet,contentDetails,status', id=video_id).execute()
    except HttpError as e:
        print('An error occurred while getting video information:', e)
        exit()

    license_type = video_info['items'][0]['status']['license']
    is_licensed_content = video_info['items'][0]['contentDetails']['licensedContent']

    
    if license_type=='creativeCommon':
        note_box_license_1.description = f"Video has a CreativeCommon license. But it is not possible to directly determine if a video on YouTube has a public domain (CC0) or Attribute (CC-BY). However, you can look for clues in the video's title or description, which may include information about the license. Many creators who use CreativeCommons will include information about the license in the title or description of their videos.\nIf video has BY (Attribution) right, it is necessary to give the author or licensor the credits (attribution) in the manner specified by these. "
    elif license_type=='youtube':
        note_box_license_1.description = "Video has a standard YouTube license. Under the Standard YouTube License, viewers are allowed to watch the video on YouTube, share the video with others using YouTube's share features, and embed the video on other websites. However, any reproduction, modification, or distribution of the video outside of these terms is prohibited without the creator's explicit permission. "
    else:
        raise RuntimeError('Unknown license type.')
    
    if is_licensed_content:
        note_box_license_2.description = 'Video has a licensed content in it. Be aware to upload data with stored licensed data in further projects.'
        

    video_info_meta = {
        'license_type' : license_type,
        'is_licensed_content' : is_licensed_content,
        'duration_sec' : duration_to_seconds(
            video_info['items'][0]['contentDetails']['duration'] 
        ),
        'author' : video_info['items'][0]['snippet']['channelTitle'],
        'description' : video_info['items'][0]['snippet']['description'],
        'title' : video_info['items'][0]['snippet']['title'],
    }


    print(f'Received YouTube meta data is:\n{video_info_meta}')
    return video_info_meta


def make_trim(input_path, output_path, start_time:int=30, end_time:int=60):
    
    input_stream = ffmpeg.input(input_path)

    vid = (
        input_stream.video
        .trim(start=start_time, end=end_time)
        .setpts('PTS-STARTPTS')
    )
    aud = (
        input_stream.audio
        .filter_('atrim', start=start_time, end=end_time)
        .filter_('asetpts', 'PTS-STARTPTS')
    )

    joined = ffmpeg.concat(vid, aud, v=1, a=1).node
    output = ffmpeg.output(joined[0], joined[1], output_path)
    ffmpeg.run(output, overwrite_output=True)


    print('Video succesfully trimmed!')
    