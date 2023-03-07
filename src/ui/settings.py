from supervisely.app.widgets import (
    Button, Select, SelectProject, SelectDataset, 
    Container, VideoThumbnail, Card, Text, Empty, Checkbox
)

import os
from dotenv import load_dotenv
import supervisely as sly

load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

project_id = sly.env.project_id()
dataset_id = sly.env.dataset_id()

button_api_upload = Button(text="Upload to Supervisely")

select_project = SelectProject(compact=True)
select_dataset = SelectDataset(project_id=project_id, compact=True)

destinations = [
    Select.Item(value="current", label="Current project & dataset"),
    Select.Item(value="new", label="New project & dataset"),
]

text_destination = Text('Choose Destination')
select_destination = Select(
    items = destinations,
    filterable=True,
)

checkbox_new_destination = Checkbox('New project & dataset')

container_destination = Container(
    widgets=[
        text_destination,
        select_destination
    ],
    direction="vertical",
)


container_project_dataset = Container(
    widgets=[
        select_project,
        select_dataset,
        Empty()
    ],
    direction="horizontal",
    fractions=[1,1,2]
)

trimmed_video_thumbnail = VideoThumbnail()

card_3 = Card(
    title="Push to supervisely",
    content=Container(widgets=[
        # container_destination,
        checkbox_new_destination, 
        container_project_dataset,
        button_api_upload, 
        trimmed_video_thumbnail ,
    ]),
)