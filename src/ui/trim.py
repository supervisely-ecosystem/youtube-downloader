import os

import src.globals as g

from supervisely.app.widgets import (
    Button, Text, Container, Card, Empty, Field, VideoPlayer
)

from src.ui.upload import card_3
from src.utils import make_trim, input_duration_to_seconds

from src.ui._common_widgets import (
    checkbox_notrim, done_text_download, done_text_trim, 
    input_min_hours, input_min_minutes, input_min_seconds, 
    input_max_hours, input_max_minutes, input_max_seconds, video_player
)

field_min_hrs = Field(content=input_min_hours, title="", description='Hours')
field_min_mnt = Field(content=input_min_minutes, title="", description='Minutes')
field_min_sec = Field(content=input_min_seconds, title="", description='Seconds')

container_min_input_time = Container(
    widgets=[
        field_min_hrs, field_min_mnt, field_min_sec, Empty()
    ],
    direction="horizontal",
    fractions=[1,1,1,6]
)

field_start_trim_time = Field(content=container_min_input_time, title='Start')

field_max_hrs = Field(content=input_max_hours, title="", description='Hours')
field_max_mnt = Field(content=input_max_minutes, title="", description='Minutes')
field_max_sec = Field(content=input_max_seconds, title="", description='Seconds')

container_max_input_time = Container(
    widgets=[
        field_max_hrs, field_max_mnt, field_max_sec, Empty()
    ],
    direction="horizontal",
    fractions=[1,1,1,6]
)

field_end_trim_time = Field(content=container_max_input_time, title='End')

button_trim = Button(text="Trim")

card_2 = Card(
    title="Video settings",
    content=Container(widgets=[
        checkbox_notrim, 
        video_player,
        field_start_trim_time,
        field_end_trim_time,
        button_trim, 
        done_text_trim,
    ]),
)

# card 2
done_text_trim.hide()
video_player.hide()
button_trim.disable()

# container_min_input_time.disable()
# container_max_input_time.disable()

input_min_hours.disable()
input_min_minutes.disable()
input_min_seconds.disable() 
input_max_hours.disable()
input_max_minutes.disable()
input_max_seconds.disable()


@checkbox_notrim.value_changed
def notrim(value):
    if value == True:
        button_trim.disable()
        input_min_hours.disable()
        input_min_minutes.disable()
        input_min_seconds.disable() 
        input_max_hours.disable()
        input_max_minutes.disable()
        input_max_seconds.disable()
        video_player.hide()
        card_3.unlock()
    else:
        button_trim.enable()
        input_min_hours.enable()
        input_min_minutes.enable()
        input_min_seconds.enable() 
        input_max_hours.enable()
        input_max_minutes.enable()
        input_max_seconds.enable()
        video_player.show()
        card_3.lock('Please trim the video')

@button_trim.click
def trim_video():

    # check status
    if not done_text_download.status=='success':
        raise RuntimeError('Video was not downloaded')

    done_text_trim.hide()

    start_time = input_duration_to_seconds(
        input_min_hours.get_value(),
        input_min_minutes.get_value(),
        input_min_seconds.get_value()
    )
    end_time = input_duration_to_seconds(
        input_max_hours.get_value(),
        input_max_minutes.get_value(),
        input_max_seconds.get_value()
    )

    yt_video_id = g.YT_VIDEO_ID

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
