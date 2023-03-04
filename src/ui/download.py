from supervisely.app.widgets import Button, Input, Select, Checkbox, Container

from supervisely.app.widgets import Text, NotificationBox, Progress

input_text = Input(placeholder="Please input a link to your video")
button_download = Button(text="Download")

licenses = [
    Select.Item(value="CC_BY", label="Creative Commons Attribution License (CC BY)"),
    Select.Item(value="CC_BY-SA", label="Creative Commons Attribution-ShareAlike License (CC BY-SA)"),
    Select.Item(value="CC_BY-NC", label="Creative Commons Attribution-NonCommercial License (CC BY-NC)"),
    Select.Item(value="CC_BY-NC-SA", label="Creative Commons Attribution-NonCommercial-ShareAlike License (CC BY-NC-SA)"),
    Select.Item(value="CC_BY-ND", label="Creative Commons Attribution-NoDerivs License (CC BY-ND)"),
    Select.Item(value="CC0", label="Creative Commons Public Domain Dedication (CC0)"),
]

select_licenses = Select(
    items = licenses,
    filterable=True,
)

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

done_text = Text()

note_box_license = NotificationBox(
    title="Notice of Potential License Infringement!",
    box_type="warning",
)

progress_bar = Progress(message="My progress message", show_percents=True)
button_stop_download = Button(text="Stop")