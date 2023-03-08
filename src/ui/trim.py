import os

import src.globals as g

from supervisely.app.widgets import (
    Button, Text, Container, Card, Empty, Field
)

from src.ui.upload import card_3
from src.utils import make_trim

from src.ui._common_widgets import (
    checkbox_notrim, done_text_download, done_text_trim, 
    input_min_seconds, input_max_seconds
)


text_min_seconds = Text(text="Start second", status="text")
text_max_seconds = Text(text="End second", status="text")

field_min_sec = Field(content=input_min_seconds, title="Start second")
field_max_sec = Field(content=input_max_seconds, title="Start second")


container_trim_interval = Container(
    widgets=[
        field_min_sec,
        field_max_sec,
        Empty()
    ],
    direction="horizontal",
    fractions=[1,1,4]
)

button_trim = Button(text="Trim")

card_2 = Card(
    title="Video settings",
    content=Container(widgets=[
        checkbox_notrim, 
        container_trim_interval,
        button_trim, 
        done_text_trim,

    ]),
)

# card 2
done_text_trim.hide()

@checkbox_notrim.value_changed
def notrim(value):
    if value == True:
        button_trim.disable()
        input_min_seconds.disable()
        input_max_seconds.disable()
        card_3.unlock()
    else:
        button_trim.enable()
        input_min_seconds.enable()
        input_max_seconds.enable()
        card_3.lock('Please trim the video')

@button_trim.click
def trim_video():

    # check status
    if not done_text_download.status=='success':
        raise RuntimeError('Video was not downloaded')

    done_text_trim.hide()

    start_time = input_min_seconds.get_value()
    end_time = input_max_seconds.get_value()

    yt_video_id = g.yt_video_id

    input_path = os.path.join(
        os.getcwd(), f'src/videos/{yt_video_id}.mp4'
    )
    output_path = os.path.join(
        os.getcwd(), f'src/videos/trimmed_{yt_video_id}.mp4'
    )

    make_trim(
        input_path=input_path,
        output_path=output_path,
        start_time=start_time,
        end_time=end_time
    )

    done_text_trim.status = 'success'
    done_text_trim.show()
    card_3.unlock()
