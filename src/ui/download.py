from supervisely.app.widgets import (
    Button, Input, Checkbox, Container, Card,
    Empty,  Text, NotificationBox, Progress
)

input_text = Input(placeholder="Please input a link to your video in format 'https://www.youtube.com/...'")


text_meta = Text(text='Add meta')

checkbox_title = Checkbox(content="Title")
checkbox_description = Checkbox(content="Description")
checkbox_author = Checkbox(content="Author", checked=True)
checkbox_author.disable()


container_meta = Container(
    widgets=[
        checkbox_title,
        checkbox_description,
        checkbox_author,
        Empty()
    ],
    direction="horizontal",
    fractions=[.7,1,1,4]
)

text_notrim = Text('Optional')
checkbox_notrim = Checkbox('Do not trim the video')


button_download = Button(text="Download")


done_text_download = Text()

note_box_license = NotificationBox(
    title="Notice of Potential License Infringement!",
    box_type="warning",
)

progress_bar = Progress(message="My progress message", show_percents=True)
button_stop_download = Button(text="Stop")

container_hidden_elements = Container(
    widgets=[
        note_box_license, 
        progress_bar, button_stop_download,
        done_text_download
    ],
    direction="vertical",
    gap=3
)


card_1 = Card(
    title="Pull video from Youtube",
    content=Container(widgets=[
        input_text, 
        text_meta,
        container_meta,
        text_notrim,
        checkbox_notrim, 
        button_download,
        container_hidden_elements,
    ]),
)