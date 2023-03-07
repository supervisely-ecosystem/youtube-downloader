import os

from supervisely.app.widgets import (
    Button, DestinationProject, 
    Container, VideoThumbnail, Card, Empty
)

import os, json
from dotenv import load_dotenv
import supervisely as sly

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()

project_id = sly.env.project_id()
dataset_id = sly.env.dataset_id()


button_api_upload = Button(text="Upload to Supervisely")


destination = DestinationProject(
    workspace_id= sly.env.workspace_id(), 
    project_type="videos", 
)


container_destination = Container(
    widgets=[
        destination,
        Empty()
    ],
    direction="horizontal",
    fractions=[1,2]
)

trimmed_video_thumbnail = VideoThumbnail()

card_3 = Card(
    title="Push to supervisely",
    content=Container(widgets=[
        # container_destination,
        # checkbox_new_destination, 
        container_destination,
        # destination,
        button_api_upload, 
        trimmed_video_thumbnail,
    ]),
)

# card 3
trimmed_video_thumbnail.hide()

@button_api_upload.click
def upload():

    
    download_status = os.environ['download_status']
    trim_status = os.environ['trim_status']
    # Checking statuses
    if not download_status == 'success':
        raise RuntimeError('Video was not downloaded.')
    if (not trim_status == 'success')\
        and (not bool(int(os.environ['is_notrim']))):
        raise RuntimeError('Video was not trimmed.')

    workspace_id = sly.env.workspace_id()

    # if destination.get_project_name() == '':
    #     raise RuntimeError('Please enter project name')
    # if destination.get_dataset_name() == '':
    #     raise RuntimeError('Please enter dataset name')

    project_id = destination.get_selected_project_id()
    if project_id is None:
        project = api.project.create(
            workspace_id=workspace_id,
            name=destination.get_project_name(),
            type=sly.ProjectType.VIDEOS,
            change_name_if_conflict=True,
        )
        project_id = project.id

    dataset_id = destination.get_selected_dataset_id()
    if dataset_id is None:
        dataset = api.dataset.create(
            project_id=project_id, 
            name=destination.get_dataset_name(), 
            change_name_if_conflict=True
        )
        dataset_id = dataset.id

    yt_video_id = os.environ['yt_video_id']

    if bool(int( os.environ['is_notrim'] )):
        video_name = f"{yt_video_id}.mp4"
    else:
        video_name = f"trimmed_{yt_video_id}.mp4"

    video_path = os.path.join(
        os.getcwd(),
        f'src/videos/{video_name}'
    )
   
    print(f"Project ID: {project_id}")
    print(f"Dataset ID: {dataset_id}")

    meta_dict = json.loads(os.environ['meta_dict'])
 
    video = api.video.upload_path(
        dataset_id,
        name=video_name,
        path=video_path,
        # meta=meta_dict 
    )

    # Add meta
    api.video.update_custom_data(id=video.id, data=meta_dict)

    video_info = api.video.get_info_by_id(id=video.id)
    trimmed_video_thumbnail.set_video(video_info)
    trimmed_video_thumbnail.show()

    print(f'Video "{video.name}" uploaded to Supervisely with ID:{video.id}')
