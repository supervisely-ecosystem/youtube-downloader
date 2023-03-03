from supervisely.app.widgets import Button, Input, InputNumber, Select, Checkbox, VideoThumbnail, Progress, Text, Container, DoneLabel

input_text = Input(placeholder="Please input a link to your video")
button_download = Button(text="Download")

licenses = [
    Select.Item(value="Public domain", label="Public domain"),
    Select.Item(value="Creative Commons", label="Creative Commons"),
    Select.Item(value="Copyleft", label="Copyleft"),
]

select_licenses = Select(
    items = licenses,
    filterable=True,
)

destinations = [
    Select.Item(value="current", label="Current project & dataset"),
    Select.Item(value="new", label="New project & dataset"),
]

select_destination = Select(
    items = destinations,
    filterable=True,
)

# checkboxes
checkbox_title = Checkbox(content="Title")
checkbox_description = Checkbox(content="Description")
checkbox_author = Checkbox(content="Author")


buttons_container_1 = Container(
    widgets=[
        button_download,        
        select_licenses,
        checkbox_title,
        checkbox_description,
        checkbox_author
    ],
    direction="horizontal",
)

done_label_download = DoneLabel('YouTube video was succesfully downloaded.')



###################

button_trim = Button(text="Trim")
input_min_seconds = InputNumber()
input_max_seconds = InputNumber()

text_min_seconds = Text(text="Start second", status="text")
text_max_seconds = Text(text="End second", status="text")

buttons_container_2 = Container(
    widgets=[
        button_trim,
        text_min_seconds,
        input_min_seconds,
        text_max_seconds,
        input_max_seconds
    ],
    direction="horizontal",
)

done_label_trim = DoneLabel('Video was succesfully trimmed.')

##################

button_api_upload = Button(text="Upload to Supervisely")

done_label_upload = DoneLabel('Video was succesfully uploaded to supervisely projects.')