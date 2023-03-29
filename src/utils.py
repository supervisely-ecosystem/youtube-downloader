import re
from multiprocessing import Manager

import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from moviepy.video.io.VideoFileClip import VideoFileClip
import yt_dlp

import src.globals as g


class Downloader:
    def __init__(self, url):
        self.url = url
        self.ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4+best[height<=480]",
            "outtmpl": "src/videos/%(id)s.%(ext)s",
            "progress_hooks": [self.progress_hook],
        }
        manager = Manager()
        self.download_info = manager.dict({"status": "downloading", "percent": 0.0})

    def run(self):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url])

    def progress_hook(self, progress):
        if progress["status"] == "downloading":
            match = re.search(r"\d+\.\d+%", progress["_percent_str"])
            percent_str = match.group()
            percent = float(percent_str.strip("%"))
            self.download_info["percent"] = percent
        elif progress["status"] == "finished":
            self.download_info["status"] = "complete"
            self.download_info["percent"] = 100.0

    def is_download_complete(self):
        return self.download_info["status"] == "complete"


def check_connection(url, name):
    response = requests.get(url)

    if response.status_code == 200:
        print("Connection successful!")
        return ["success", f"Connection to {name} successful!"]
    else:
        print(f"Connection failed with status code: {response.status_code}")
        return [
            "error",
            f"Failed to establish connection to {name}. (Status code: {response.status_code})",
        ]


def get_youtube_id(link):
    try:
        video_id = re.search(r"(?<=v=)[^&#]+", link).group(0)
    except AttributeError:
        raise ValueError("Invalid YouTube link.")

    print(f"Youtube ID is {video_id}")
    return video_id


def duration_to_seconds(duration):
    """Converts a YouTube video duration from ISO 8601 format to seconds."""
    match = re.match("PT(\d+H)?(\d+M)?(\d+S)?", duration).groups()
    hours = int(match[0][:-1]) if match[0] else 0
    minutes = int(match[1][:-1]) if match[1] else 0
    seconds = int(match[2][:-1]) if match[2] else 0
    return hours * 3600 + minutes * 60 + seconds


def get_meta(video_id, note_box_license_1, note_box_license_2):

    # Set up the API client
    youtube = build("youtube", "v3", developerKey=g.YT_API_KEY)

    # Get the video information
    try:
        video_info = (
            youtube.videos().list(part="snippet,contentDetails,status", id=video_id).execute()
        )
    except HttpError as e:
        print("An error occurred while getting video information:", e)
        exit()

    license_type = video_info["items"][0]["status"]["license"]
    is_licensed_content = video_info["items"][0]["contentDetails"]["licensedContent"]

    if license_type == "creativeCommon":
        note_box_license_1.description = f"Video has a CreativeCommon license. But it is not possible to directly determine if a video on YouTube has a public domain (CC0) or Attribute (CC-BY). However, you can look for clues in the video's title or description, which may include information about the license. Many creators who use CreativeCommons will include information about the license in the title or description of their videos.\nIf video has BY (Attribution) right, it is necessary to give the author or licensor the credits (attribution) in the manner specified by these. "
    elif license_type == "youtube":
        note_box_license_1.description = "Video has a standard YouTube license. Under the Standard YouTube License, viewers are allowed to watch the video on YouTube, share the video with others using YouTube's share features, and embed the video on other websites. However, any reproduction, modification, or distribution of the video outside of these terms is prohibited without the creator's explicit permission. "
    else:
        raise RuntimeError("Unknown license type.")

    if is_licensed_content:
        note_box_license_2.description = "Video has a licensed content in it. Be aware to upload data with stored licensed data in further projects."

    video_info_meta = {
        "license_type": license_type,
        "is_licensed_content": is_licensed_content,
        "duration": video_info["items"][0]["contentDetails"]["duration"],
        "duration_sec": duration_to_seconds(video_info["items"][0]["contentDetails"]["duration"]),
        "author": video_info["items"][0]["snippet"]["channelTitle"],
        "description": video_info["items"][0]["snippet"]["description"],
        "title": video_info["items"][0]["snippet"]["title"],
    }

    print(f"Received YouTube meta data is:\n{video_info_meta}")
    return video_info_meta


def make_trim(input_path, output_path, start_time, end_time):
    with VideoFileClip(input_path) as video:
        trimmed_clip = video.subclip(start_time, end_time)
        trimmed_clip.write_videofile(output_path)
