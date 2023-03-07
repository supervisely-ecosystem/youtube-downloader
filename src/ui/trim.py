from supervisely.app.widgets import (
    Button, InputNumber, Text, Container, DoneLabel, Card, Empty
)

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

card_2 = Card(
    title="Trim video",
    content=Container(widgets=[
    
    container_trim_interval,
    button_trim, 
    done_text_trim,

    ]),
)