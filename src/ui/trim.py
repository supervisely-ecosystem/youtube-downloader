import os

import src.globals as g

from supervisely.app.widgets import Button, Container, Card, Empty

from src.ui.upload import card_3
from src.utils import make_trim

from src.ui._common_widgets import (
    checkbox_notrim,
    done_text_download,
    done_text_trim,
    video_player,
    slider,
    field_slider,
    trimming_range_float,
)


button_start = Button(text="Set start", button_type="info", button_size="small")
button_end = Button(text="Set end", button_type="info", button_size="small")

container_set_buttons = Container(
    widgets=[button_start, button_end, Empty()], direction="horizontal", fractions=[1, 1, 6]
)


button_trim = Button(text="Trim segment")


container_hidden_elements = Container(
    widgets=[
        video_player,
        container_set_buttons,
    ],
    direction="vertical",
)

card_2 = Card(
    title="Trim settings",
    content=Container(
        widgets=[
            checkbox_notrim,
            container_hidden_elements,
            field_slider,
            button_trim,
            done_text_trim,
        ]
    ),
)


# card 2
container_hidden_elements.hide()
video_player.hide()
container_set_buttons.hide()
button_trim.disable()
slider.disable()
done_text_trim.hide()


@button_start.click
def set_start():
    curr_range = slider.get_value()
    if video_player.get_current_timestamp() <= curr_range[1]:
        slider.set_value([int(video_player.get_current_timestamp()), curr_range[1]])
    else:
        slider.set_value(
            [
                int(video_player.get_current_timestamp()),
                int(video_player.get_current_timestamp()),
            ]
        )
    trimming_range_float["start"] = video_player.get_current_timestamp()


@button_end.click
def set_end():
    curr_range = slider.get_value()
    if video_player.get_current_timestamp() >= curr_range[0]:
        slider.set_value(
            [
                curr_range[0],
                int(video_player.get_current_timestamp()),
            ]
        )
    else:
        slider.set_value(
            [
                int(video_player.get_current_timestamp()),
                int(video_player.get_current_timestamp()),
            ]
        )
    trimming_range_float["end"] = video_player.get_current_timestamp()


@checkbox_notrim.value_changed
def notrim(value):
    if value == True:
        container_hidden_elements.hide()
        button_trim.disable()
        slider.disable()
        video_player.hide()
        container_set_buttons.hide()
        card_3.unlock()
    else:
        container_hidden_elements.show()
        button_trim.enable()
        slider.enable()
        video_player.show()
        container_set_buttons.show()
        card_3.lock("Please trim the video")


@button_trim.click
def trim_video():

    # check status
    if not done_text_download.status == "success":
        raise RuntimeError("Video was not downloaded")

    done_text_trim.hide()

    yt_video_id = g.YT_VIDEO_ID

    input_path = os.path.join(os.getcwd(), f"src/videos/{yt_video_id}.mp4")
    output_path = os.path.join(os.getcwd(), f"src/videos/trimmed_{yt_video_id}.mp4")

    make_trim(
        input_path=input_path,
        output_path=output_path,
        start_time=trimming_range_float["start"],
        end_time=trimming_range_float["end"],
    )

    done_text_trim.status = "success"
    done_text_trim.show()
    card_3.unlock()
