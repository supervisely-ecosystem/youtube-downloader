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


sly_file = sly.env.file()

storage_dir = sly.app.get_data_dir()

api.file.download(
    TEAM_ID, sly_file, 
    os.path.join(storage_dir,os.path.basename(sly_file))
)

# sly_file = None # for debug

if sly_file == None or sly_file == "":
    YT_API_KEY = None
else:
    with open(
        os.path.join(storage_dir,os.path.basename(sly_file)), "r"
    ) as f:
        dct = json.load(f)
        YT_API_KEY = dct['YT_API_KEY']

YT_VIDEO_ID = None
META_DICT = None
LICENSES = ['youtube', 'creativeCommon']