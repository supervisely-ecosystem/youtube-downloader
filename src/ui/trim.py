import os

import src.globals as g

from supervisely.app.widgets import (
    Button, Container, Card, Field
)

from src.ui.upload import card_3
from src.utils import make_trim

from src.ui._common_widgets import (
    checkbox_notrim, done_text_download, done_text_trim, 
    video_player, slider, field_slider
)

    


button_trim = Button(text="Trim selected segment")

card_2 = Card(
    title="Video settings",
    content=Container(widgets=[
        checkbox_notrim, 
        video_player,
        field_slider,
        button_trim, 
        done_text_trim,
    ]),
)

# card 2
done_text_trim.hide()
video_player.hide()
button_trim.disable()
slider.disable()


@checkbox_notrim.value_changed
def notrim(value):
    if value == True:
        button_trim.disable()
        slider.disable()
        video_player.hide()
        card_3.unlock()
    else:
        button_trim.enable()
        slider.enable()
        video_player.show()
        card_3.lock('Please trim the video')

@button_trim.click
def trim_video():

    # check status
    if not done_text_download.status=='success':
        raise RuntimeError('Video was not downloaded')

    done_text_trim.hide()

    start_time, end_time = slider.get_value()

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
