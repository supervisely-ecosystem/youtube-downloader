import os, json

import supervisely as sly
from dotenv import load_dotenv

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api: sly.Api = sly.Api.from_env()

TEAM_ID = sly.env.team_id()
# WORKSPACE_ID = sly.env.workspace_id()
# PROJECT_ID = sly.env.project_id()
# DATASET_ID = sly.env.dataset_id(raise_not_found=False)


sly_file = sly.env.file(raise_not_found=False)

if sly_file is None:
    YT_API_KEY = None
else:
    storage_dir = sly.app.get_data_dir()
    file_path = os.path.join(storage_dir, os.path.basename(sly_file))

    api.file.download(TEAM_ID, sly_file, file_path)

    # sly_file = None  # for debug of manual input of yt api key

    if sly_file == None or sly_file == "":
        YT_API_KEY = None
    else:
        file_ext = os.path.splitext(sly_file)[1].lower()

        if file_ext == ".env":
            load_dotenv(file_path)
            YT_API_KEY = os.getenv("YT_API_KEY")
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")


# YT_VIDEO_LINK = None
YT_VIDEO_ID = None
META_DICT = None
LICENSES = ["youtube", "creativeCommon"]
