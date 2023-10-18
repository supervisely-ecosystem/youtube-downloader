import os
import json
import time
import traceback
from multiprocessing import Process

from supervisely.app.widgets import (
    Button,
    Input,
    Checkbox,
    Container,
    Card,
    Empty,
    Field,
)

import src.globals as g
from src.ui._common_widgets import (
    container_hidden_elements,
    text_check_input_ytlink,
    done_text_download,
    progress_bar,
    note_box_license_1,
    note_box_license_2,
    video_player,
    slider,
    field_slider,
    trimming_range_float,
)
from src.ui.trim import card_2
from src.ui.upload import card_3
from src.utils import get_youtube_id, get_meta, Downloader


input_yt_link = Input(
    placeholder="Please input a link to your video in 'https://www.youtube.com/...' or 'https://youtu.be/...' format"
)


field_available_licenses = Field(
    content=Empty(),
    title="",
    description="Available licenses: 1) YouTube license, 2) Creative Commons",
)


checkbox_title = Checkbox(content="Title")
checkbox_description = Checkbox(content="Description")
checkbox_author = Checkbox(content="Author", checked=True)
checkbox_author.disable()


container_meta = Container(
    widgets=[
        checkbox_title,
        checkbox_description,
        checkbox_author,
        Empty(),
    ],
    direction="horizontal",
    fractions=[0.5, 1, 1, 8],
)

field_meta = Field(content=container_meta, title="Add meta")


button_download = Button(text="Download")
button_stop_download = Button(text="Stop", button_type="danger")

container_buttons = Container(
    widgets=[button_download, button_stop_download, Empty()],
    direction="horizontal",
    fractions=[1, 0.8, 5],
)


card_1 = Card(
    title="Video Settings",
    content=Container(
        widgets=[
            input_yt_link,
            text_check_input_ytlink,
            field_available_licenses,
            field_meta,
            container_buttons,
            container_hidden_elements,
        ]
    ),
)

# card 1 states
button_stop_download.hide()
text_check_input_ytlink.hide()
container_hidden_elements.hide()

card_2.lock(message="Please download video first")
card_3.lock(message="Please download video first")


@button_download.click
def download_video():
    link = input_yt_link.get_value()
    # check statuses
    if link == "":
        text_check_input_ytlink.text = "Input form is empty. Please input YouTube link."
        text_check_input_ytlink.status = "error"
        text_check_input_ytlink.show()
        return None
    if not link.startswith(g.LINK_PREFIX_LONG) or not link.startswith(g.LINK_PREFIX_SHORT):
        text_check_input_ytlink.text = "Invalid YouTube link. Make sure it starts with 'https://www.youtube.com/...' or 'https://youtu.be/...'"
        text_check_input_ytlink.status = "error"
        text_check_input_ytlink.show()
        return None
    else:
        text_check_input_ytlink.hide()

    progress_bar.hide()
    done_text_download.hide()
    note_box_license_1.hide()
    note_box_license_2.hide()
    container_hidden_elements.show()

    yt_video_id = get_youtube_id(link)
    g.YT_VIDEO_ID = str(yt_video_id)

    meta_dict_2save = {
        "license_type": True,
        "is_licensed_content": True,
        "duration": False,
        "duration_sec": False,
        "author": checkbox_author.is_checked(),
        "description": checkbox_description.is_checked(),
        "title": checkbox_title.is_checked(),
    }

    full_meta_dict = get_meta(yt_video_id, note_box_license_1, note_box_license_2)

    meta_dict_2save = {key: value for key, value in full_meta_dict.items() if meta_dict_2save[key]}

    meta_dict_2save["youtube_link"] = input_yt_link.get_value()
    meta_dict_2save["youtube_id"] = yt_video_id

    g.META_DICT = json.dumps(meta_dict_2save)

    if not note_box_license_1.description == None:
        note_box_license_1.show()
    if not note_box_license_2.description == None:
        note_box_license_2.show()

    filename = os.path.join(os.getcwd(), f"src/videos/{yt_video_id}.mp4")

    if os.path.exists(filename):
        done_text_download.text = f'Video "{full_meta_dict["title"]}" was already downloaded.'
        done_text_download.status = "success"
        done_text_download.show()
    else:
        print("Getting Video...")

        if not os.path.exists("src/videos/"):
            os.makedirs("src/videos/")

        progress_bar.show()
        button_stop_download.show()

        with progress_bar(message=f"Downloading video...", total=100) as pbar:

            global is_stopped
            is_stopped = False

            url = f"{g.LINK_PREFIX_LONG}{yt_video_id}"

            d = Downloader(url)
            p = Process(target=d.run)
            p.start()

            try:
                increment = 0
                while True:

                    prev = d.download_info["percent"]

                    time.sleep(1)

                    increment = d.download_info["percent"] - prev
                    pbar.update(increment)

                    if is_stopped:
                        p.terminate()
                        print("Download stopped")

                        done_text_download.text = "Video download was stopped."
                        done_text_download.status = "warning"
                        done_text_download.show()
                        button_stop_download.hide()
                        return None

                    if d.is_download_complete():
                        print("Download complete")
                        p.join()
                        done_text_download.text = (
                            f'Video "{full_meta_dict["title"]}" was succesfully downloaded.'
                        )
                        done_text_download.status = "success"
                        done_text_download.show()
                        break

            except Exception as e:
                traceback.print_exc()
                print("An error occurred while downloading the video:", e)

    button_stop_download.hide()
    print(
        "Video downloaded to directory:", os.path.join(os.getcwd(), f"src/videos/{yt_video_id}.mp4")
    )

    video_player.set_video(f"static/{yt_video_id}.mp4")

    slider.set_min(0)
    slider.set_max(full_meta_dict["duration_sec"])
    slider.set_value([0, int(full_meta_dict["duration_sec"] / 5)])

    trimming_range_float["end"] = full_meta_dict["duration_sec"] / 5
    trimming_range_float["full"] = full_meta_dict["duration_sec"]

    field_slider._description = f"""
    Full video: {int(trimming_range_float["full"])} seconds. Segment: {int(trimming_range_float["full"] / 5)} seconds
    """
    field_slider.update_data()

    card_2.unlock()
    card_3.unlock()


@button_stop_download.click
def stop_download():

    global is_stopped
    is_stopped = True
