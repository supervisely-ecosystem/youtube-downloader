import os, re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pytube import YouTube

import ffmpeg

# def percent(self, tem, total):
#         perc = (float(tem) / float(total)) * float(100)
#         return perc

# def progress_function(stream, chunk, bytes_remaining):

#     size = stream.filesize
#     p = 0
#     while p <= 100:
#         progress = p
#         print(str(p)+'%')
#         pbar.update(1)
#         p = percent(bytes_remaining, size)

import sys

# from src.main import progress_bar


def progress_callback(stream, chunk, bytes_remaining):
    # Calculate the percentage of the file that has been downloaded
    percent = (100 * (stream.filesize - bytes_remaining)) / stream.filesize
    # Create a progress bar with '=' characters for completed chunks and '-' characters for incomplete chunks
    progress_bar = '[' + '=' * int(percent / 2) + '-' * int((100 - percent) / 2) + ']'
    # Print the progress bar and the percentage of completion
    sys.stdout.write('\r' + progress_bar + ' {:.2f}%'.format(percent))
    sys.stdout.flush()

# def progress_function(stream, chunk, bytes_remaining):
#     total_size = stream.filesize
#     bytes_downloaded = total_size - bytes_remaining
#     percent_complete = bytes_downloaded / total_size * 100
#     progress_bar.update(int(percent_complete))
#     print(f"{percent_complete:.2f}% downloaded")

def get_video(link):
    # Replace with your API key
    API_KEY = "AIzaSyCi-0otAqE59rywdfx0IdrMzP5niYWk_uo"

    # Set up the API client
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    assert link.startswith("https://www.youtube.com/"), "Invalid YouTube link"
    try:
        # Extract the video ID from the link using regular expressions
        video_id = re.search(r'(?<=v=)[^&#]+', link).group(0)
    except AttributeError:
        # If the regular expression doesn't match, raise an exception with a custom error message
        raise ValueError("Invalid YouTube link")
    
    # Set up the video ID and time interval
    # video_id = link.split('watch?v=')[1]

    # Get the video information
    try:
        video_info = youtube.videos().list(part='snippet,contentDetails', id=video_id).execute()
        video_title = video_info['items'][0]['snippet']['title']
        video_duration = video_info['items'][0]['contentDetails']['duration']
    except HttpError as e:
        print('An error occurred while getting video information:', e)
        exit()

    # Download the video
    try:
        yt = YouTube(f'https://www.youtube.com/watch?v={video_id}', on_progress_callback=progress_callback)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path= os.path.join(os.getcwd(), 'src/videos'), filename=f"{video_id}.mp4")
        os.environ['video_filesize'] = str(stream.filesize)

    except Exception as e:
        print('An error occurred while downloading the video:', e)
        exit()

    print('Video downloaded successfully!')

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