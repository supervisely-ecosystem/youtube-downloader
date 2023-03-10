from supervisely.app.widgets import (
    Checkbox, Text, NotificationBox, InputNumber, VideoPlayer
)

done_text_download = Text()
done_text_trim = Text('Video was succesfully trimmed.')

input_min_hours = InputNumber(value=0, min=0)
input_min_minutes = InputNumber(value=0, min=0)
input_min_seconds = InputNumber(value=0, min=0)

input_max_hours = InputNumber(value=0, min=0)
input_max_minutes = InputNumber(value=0, min=0)
input_max_seconds = InputNumber(value=0, min=0)

note_box_license_1 = NotificationBox(
    title="Notice of Potential License Infringement!",
    box_type="warning",
)

note_box_license_2 = NotificationBox(
    title="Notice of Potential License Infringement!",
    box_type="warning",
)

checkbox_notrim = Checkbox('Do not trim the video', checked=True)

video_player = VideoPlayer()