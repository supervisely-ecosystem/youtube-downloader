from supervisely.app.widgets import (
    Checkbox,
    Container,
    Field,
    Flexbox,
    Icons,
    Input,
    NotificationBox,
    Progress,
    Text,
    VideoPlayer,
    Slider,
)

input_yt_API_KEY = Input(placeholder="Please input YouTube v3 API KEY", type="password")

text_check_input_ytlink = Text()
text_check_input_ytapi = Text()
text_check_input_ytapi_icon = Icons(class_name="zmdi zmdi-n-2-square", color="#009aff", bg_color="#ffffff")
text_check_input_ytapi_box = Flexbox(widgets=[text_check_input_ytapi, text_check_input_ytapi_icon])


done_text_download = Text()
done_text_trim = Text("Video was succesfully trimmed.")

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
        # text_check_input_ytlink,
        progress_bar,
        note_box_license_1,
        note_box_license_2,
        done_text_download,
    ],
    direction="vertical",
)

checkbox_notrim = Checkbox("Do not trim the video", checked=True)

video_player = VideoPlayer()

slider = Slider(value=[0, 20], range=True)

trimming_range_float = {"start": 0, "end": 20, "full": 100}

field_slider = Field(
    content=slider,
    title="",
)
