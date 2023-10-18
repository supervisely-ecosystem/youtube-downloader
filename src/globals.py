import os, json

import supervisely as sly
from dotenv import load_dotenv

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api: sly.Api = sly.Api.from_env()

TEAM_ID = sly.env.team_id()

SLY_FILE = sly.env.file(raise_not_found=False)

YT_API_RUN_FROM_TF = False
YT_API_NOT_FOUND = False
YT_API_INVALID_FORMAT = False

YT_API_KEY = None
if SLY_FILE is not None and SLY_FILE != "":
    YT_API_RUN_FROM_TF = True
    if not api.file.exists(TEAM_ID, SLY_FILE):
        sly.logger.warn(f"File {SLY_FILE} not found in team files")
        YT_API_NOT_FOUND = True
    else:
        storage_dir = sly.app.get_data_dir()
        file_path = os.path.join(storage_dir, os.path.basename(SLY_FILE))
        api.file.download(TEAM_ID, SLY_FILE, file_path)

        file_ext = os.path.splitext(SLY_FILE)[1].lower()
        if file_ext == ".env":
            load_dotenv(file_path)
            YT_API_KEY = os.getenv("YT_API_KEY")
        else:
            YT_API_INVALID_FORMAT = True

LINK_PREFIX_LONG = "https://www.youtube.com/watch?v="
LINK_PREFIX_SHORT = "https://youtu.be/"

# YT_VIDEO_LINK = None
YT_VIDEO_ID = None
META_DICT = None
LICENSES = ["youtube", "creativeCommon"]
