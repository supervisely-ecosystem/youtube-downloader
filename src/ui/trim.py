from supervisely.app.widgets import Button, InputNumber, Text, Container, DoneLabel


button_trim = Button(text="Trim")
input_min_seconds = InputNumber()
input_max_seconds = InputNumber()


text_min_seconds = Text(text="Start second", status="text")
text_max_seconds = Text(text="End second", status="text")


buttons_container_2 = Container(
    widgets=[
        button_trim,
        text_min_seconds,
        input_min_seconds,
        text_max_seconds,
        input_max_seconds
    ],
    direction="horizontal",
)

done_label_trim = DoneLabel('Video was succesfully trimmed.')
