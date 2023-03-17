import requests

from supervisely.app.widgets import (
    Input, Container, Card, Text, Button
)

import src.globals as g

from src.utils import check_connection

from src.ui.download import card_1

from src.ui._common_widgets import text_check_input_ytapi, input_yt_API_KEY

text_source_info = Text()
text_source_info.status = 'info'
text_connection_status = Text()

if g.YT_API_KEY is None:
    text_source_info.text = 'YouTube API key should be loaded manually'
    input_yt_API_KEY.show()
else:
    text_source_info.text = 'YouTube API key is loaded from the team files.'
    input_yt_API_KEY.hide()

# checking connection
response = check_connection("https://www.youtube.com/", 'YouTube')
text_connection_status.status = response[0]
text_connection_status.text = response[1]


text_check_input_ytapi.hide()

button_check = Button(text="Check API key")

def validate_api_key(API_KEY):
            # Build the request URL with your API key and a sample API endpoint
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id=INVALID_VIDEO_ID&key={API_KEY}"

    # Make the request
    response = requests.get(url)

    # Check the response status code
    if response.status_code == 200:
        print("API key is valid.")
        text_check_input_ytapi.text = 'API key is valid'
        text_check_input_ytapi.status = 'success'
        text_check_input_ytapi.show()
        text_connection_status.show()
        return 'success'
    else:
        text_check_input_ytapi.text = 'Invalid or unauthorized API key'
        text_check_input_ytapi.status = 'error'
        text_check_input_ytapi.show()
        card_1.lock('Please check your YouTube API key first.')
        return 'error'

if g.YT_API_KEY is None:
    card_0 = Card(
        title="Source info",
        content=Container(widgets=[ 
            text_source_info,
            text_connection_status,            
            input_yt_API_KEY,
            button_check,
            text_check_input_ytapi,
        ]),
    )

    card_1.lock('Please check your YouTube API key first.')

else:
    card_0 = Card(
        title="YouTube API Token",
        content=Container(widgets=[ 
            text_source_info,
            text_connection_status,            
            text_check_input_ytapi,
        ]),
    )

    if g.YT_API_KEY =="":
        text_check_input_ytapi.text = 'Input form is empty. Please input YouTube API key.'
        text_check_input_ytapi.status = 'error'
        text_check_input_ytapi.show()
    else:
        validation = validate_api_key(g.YT_API_KEY)
        
        if validation == 'success':
            card_1.unlock()
        
# if text_connection_status.status == 'error':
#     button_check.disable()
#     input_yt_API_KEY.disable()
# else:
#     button_check.enable()
#     input_yt_API_KEY.enable()


@button_check.click
def check_api():

    if input_yt_API_KEY.get_value()=="" and g.YT_API_KEY==None:
        text_check_input_ytapi.text = 'Input form is empty. Please input YouTube API key.'
        text_check_input_ytapi.status = 'error'
        text_check_input_ytapi.show()
    else:
        validation = validate_api_key(input_yt_API_KEY.get_value())

        if validation == 'success':
            g.YT_API_KEY = input_yt_API_KEY.get_value()
            card_1.unlock()