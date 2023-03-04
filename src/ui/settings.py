from supervisely.app.widgets import Button, Select, Input, Container, VideoThumbnail


button_api_upload = Button(text="Upload to Supervisely")

destinations = [
    Select.Item(value="current", label="Current project & dataset"),
    Select.Item(value="new", label="New project & dataset"),
]

select_destination = Select(
    items = destinations,
    filterable=True,
)

input_project_id = Input(placeholder="Project ID")#, value=18007)
input_dataset_id = Input(placeholder="Dataset ID")#, value=60152)


buttons_container_3 = Container(
    widgets=[
        button_api_upload,
        select_destination,
        input_project_id,
        input_dataset_id
    ],
    direction="horizontal",
)

trimmed_video_thumbnail = VideoThumbnail()