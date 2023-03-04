from supervisely.app.widgets import Button, Input, InputNumber, Select, Checkbox, VideoThumbnail, Progress, Text, Container, DoneLabel

from supervisely.app.widgets import Text, NotificationBox


# input_text = Input(placeholder="Please input a link to your video")
# button_download = Button(text="Download")

# licenses = [
#     Select.Item(value="CC_BY", label="Creative Commons Attribution License (CC BY)"),
#     Select.Item(value="CC_BY-SA", label="Creative Commons Attribution-ShareAlike License (CC BY-SA)"),
#     Select.Item(value="CC_BY-NC", label="Creative Commons Attribution-NonCommercial License (CC BY-NC)"),
#     Select.Item(value="CC_BY-NC-SA", label="Creative Commons Attribution-NonCommercial-ShareAlike License (CC BY-NC-SA)"),
#     Select.Item(value="CC_BY-ND", label="Creative Commons Attribution-NoDerivs License (CC BY-ND)"),
#     Select.Item(value="CC0", label="Creative Commons Public Domain Dedication (CC0)"),
# ]

# select_licenses = Select(
#     items = licenses,
#     filterable=True,
# )

# checkbox_title = Checkbox(content="Title")
# checkbox_description = Checkbox(content="Description")
# checkbox_author = Checkbox(content="Author")


# buttons_container_1 = Container(
#     widgets=[
#         button_download, 
#         select_licenses,       
#         checkbox_title,
#         checkbox_description,
#         checkbox_author
#     ],
#     direction="horizontal",
# )

# done_text = Text()

# note_box_license = NotificationBox(
#     title="Notice of Potential License Infringement!",
#     box_type="warning",
# )


###################

# button_trim = Button(text="Trim")
# input_min_seconds = InputNumber()
# input_max_seconds = InputNumber()

# text_min_seconds = Text(text="Start second", status="text")
# text_max_seconds = Text(text="End second", status="text")



# buttons_container_2 = Container(
#     widgets=[
#         button_trim,
#         text_min_seconds,
#         input_min_seconds,
#         text_max_seconds,
#         input_max_seconds
#     ],
#     direction="horizontal",
# )

# done_label_trim = DoneLabel('Video was succesfully trimmed.')

##################

# destinations = [
#     Select.Item(value="current", label="Current project & dataset"),
#     Select.Item(value="new", label="New project & dataset"),
# ]

# select_destination = Select(
#     items = destinations,
#     filterable=True,
# )

# input_project_id = Input(placeholder="Project ID", value=18007)
# input_dataset_id = Input(placeholder="Dataset ID", value=60152)

# button_api_upload = Button(text="Upload to Supervisely")

# buttons_container_3 = Container(
#     widgets=[
#         button_api_upload,
#         select_destination,
#         input_project_id,
#         input_dataset_id
        
#     ],
#     direction="horizontal",
# )

