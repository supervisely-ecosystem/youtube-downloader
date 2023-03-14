from supervisely.app.widgets import (
    Checkbox, Text, NotificationBox, InputNumber, VideoPlayer,
    Slider, Container, Empty, Progress, Field, Input
)

input_yt_API_KEY = Input(
    placeholder="Please input YouTube v3 API KEY", 
    type='password'
)

done_text_download = Text()
done_text_trim = Text('Video was succesfully trimmed.')

progress_bar = Progress(show_percents=True)

note_box_license_1 = NotificationBox(
    title="Notice of Potential License Infringement!",
    box_type="warning",
)

note_box_license_2 = NotificationBox(
    title="Notice of Potential License Infringement!",
    box_type="warning",
)

container_hidden_elements = Container(
    widgets=[
        progress_bar,
        note_box_license_1, note_box_license_2,
        done_text_download,
    ],
    direction="vertical",
    # gap=0
)

input_min_hours = InputNumber(value=0, min=0)
input_min_minutes = InputNumber(value=0, min=0)
input_min_seconds = InputNumber(value=0, min=0)

input_max_hours = InputNumber(value=0, min=0)
input_max_minutes = InputNumber(value=0, min=0)
input_max_seconds = InputNumber(value=0, min=0)



checkbox_notrim = Checkbox('Do not trim the video', checked=True)

video_player = VideoPlayer()

slider = Slider(value=[0, 10], range=True)


field_slider = Field(
    content=slider, title="",
)
