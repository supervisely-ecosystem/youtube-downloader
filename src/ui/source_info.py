from supervisely.app.widgets import Button, Card, Container, Input, Text

import src.globals as g
from src.utils import check_connection, get_text_icon, validate_api_key
from src.ui.download import card_1

text_connection_status = Text()
text_check_input_ytapi = Text(status="info")
input_yt_API_KEY = Input(placeholder="Please input YouTube v3 API KEY", type="password")
button_check = Button(text="Check API key")


def valid_key_update(text):
    text_check_input_ytapi.text = get_text_icon(2) + text
    text_check_input_ytapi.status = "success"
    text_check_input_ytapi.show()
    text_connection_status.show()
    button_check.hide()
    input_yt_API_KEY.hide()
    card_1.unlock()


def invalid_key_update(text):
    text_check_input_ytapi.text = get_text_icon(2) + text
    text_check_input_ytapi.status = "error"
    text_check_input_ytapi.show()
    button_check.show()
    input_yt_API_KEY.show()
    card_1.lock("Please check your YouTube API key first.")


if g.YT_API_NOT_FOUND:
    invalid_key_update("YouTube API key is not found in the team files. Please input it manually.")
    text_check_input_ytapi.status = "error"
elif g.YT_API_INVALID_FORMAT:
    invalid_key_update("Invalid format of YouTube API key file. Please input it manually.")
elif g.YT_API_RUN_FROM_TF and g.YT_API_KEY is None:
    invalid_key_update("'YT_API_KEY' is not found in the key file. Please input it manually.")
elif g.SLY_FILE is None:
    invalid_key_update("Please input YouTube API key manually.")
elif g.YT_API_KEY == "":
    invalid_key_update("Input form is empty. Please input YouTube API key.")
elif not validate_api_key(g.YT_API_KEY):
    invalid_key_update("Invalid or unauthorized API key")
else:
    msg = "API key is loaded from the team files." if g.YT_API_RUN_FROM_TF else "API key is valid"
    valid_key_update(msg)


# checking connection
response = check_connection("https://www.youtube.com/", "YouTube")
text_connection_status.status = response[0]
text_connection_status.text = get_text_icon(1) + response[1]


card_0 = Card(
    title="YouTube API token",
    content=Container(
        widgets=[
            text_connection_status,
            text_check_input_ytapi,
            input_yt_API_KEY,
            button_check,
        ]
    ),
)


@button_check.click
def check_api():
    input_value = input_yt_API_KEY.get_value()
    if input_value == "":
        invalid_key_update("Input form is empty. Please input YouTube API key.")
    else:
        if validate_api_key(input_value):
            g.YT_API_KEY = input_value
            valid_key_update("API key is valid")
        else:
            invalid_key_update("Invalid or unauthorized API key")
