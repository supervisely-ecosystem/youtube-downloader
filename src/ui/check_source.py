from supervisely.app.widgets import (
    Button, Input, Checkbox, Container, Card,
    Empty,  Text, Progress, Field
)

from src.ui._common_widgets import input_yt_API_KEY

import src.globals as g

from src.utils import check_connection



text_source_info = Text()
text_source_info.status = 'info'
text_connection_status = Text()

# if g.YT_API_KEY is None:
#     text_source_info.text = 'YouTube API key should be loaded manually'
#     input_yt_API_KEY.show()
# else:
#     text_source_info.text = 'YouTube API key is loaded from the team files.'
#     input_yt_API_KEY.hide()

# checking connection
# response = check_connection("https://www.youtube.com/", 'YouTube')
# text_connection_status.status = response[0]
# text_connection_status.text = response[1]
text_connection_status.show()
text_connection_status.hide()

card_0 = Card(
    title="Source",
    content=Container(widgets=[ 
        input_yt_API_KEY,
        text_source_info,
        text_connection_status,
    ]),
)