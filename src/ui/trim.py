import os

from supervisely.app.widgets import (
    Button, InputNumber, Text, Container, Card, Empty
)

from src.ui.settings import card_3
from src.utils import trim

input_min_seconds = InputNumber()
input_max_seconds = InputNumber()

text_min_seconds = Text(text="Start second", status="text")
text_max_seconds = Text(text="End second", status="text")

container_left_trim = Container(
    widgets=[
        text_min_seconds,
        input_min_seconds,
    ],
    direction="vertical",
)

container_right_trim = Container(
    widgets=[
        text_max_seconds,
        input_max_seconds,
    ],
    direction="vertical",
)

container_trim_interval = Container(
    widgets=[
        container_left_trim,
        container_right_trim,
        Empty()
    ],
    direction="horizontal",
    fractions=[1,1,4]
)

button_trim = Button(text="Trim")
done_text_trim = Text('Video was succesfully trimmed.')
os.environ['trim_status'] = str(None)

card_2 = Card(
    title="Trim video",
    content=Container(widgets=[
    
    container_trim_interval,
    button_trim, 
    done_text_trim,

    ]),
)

# card 2
done_text_trim.hide()


@button_trim.click
def trim_video():

    done_text_trim.hide()

    start_time = input_min_seconds.get_value()
    end_time = input_max_seconds.get_value()

    yt_video_id = os.environ['yt_video_id']

    input_path = os.path.join(
        os.getcwd(), f'src/videos/{yt_video_id}.mp4'
    )
    output_path = os.path.join(
        os.getcwd(), f'src/videos/trimmed_{yt_video_id}.mp4'
    )

    trim(
        input_path=input_path,
        output_path=output_path,
        start=start_time,
        end=end_time
    )

    done_text_trim.status = 'success'
    done_text_trim.show()
    card_3.unlock()

    os.environ['trim_status'] = done_text_trim.status

