import os, json, re
import src.globals as g

from supervisely.app.widgets import (
    Button, Input, Checkbox, Container, Card,
    Empty,  Text, Progress, Field
)

from src.ui._common_widgets import (
    done_text_download, 
    input_min_hours, input_min_minutes, input_min_seconds, 
    input_max_hours, input_max_minutes, input_max_seconds,
    note_box_license_1, note_box_license_2, video_player
)

from src.ui.trim import card_2
from src.ui.upload import card_3

from src.utils import (
    get_youtube_id, get_meta, check_connection
)
from pytube import YouTube, request

input_yt_link = Input(placeholder="Please input a link to your video in format 'https://www.youtube.com/...'")

input_yt_API_KEY = Input(
    placeholder="Please input YouTube v3 API KEY", 
    type='password'
)

text_source_info = Text()
text_source_info.status = 'info'
text_connection_status = Text()


field_available_licenses = Field(
    content=Empty(), title="",
    description="Available licenses: 1) YouTube license, 2) Creative Commons"
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
    fractions=[.5,1,1,8],
)


field_meta = Field(content=container_meta, title="Add meta")


button_download = Button(text="Download")
button_stop_download = Button(text="Stop", button_type='danger')

container_buttons = Container(
    widgets=[
        button_download, button_stop_download, Empty()
    ],
    direction="horizontal",
    fractions=[1,1,4],
)

progress_bar = Progress(show_percents=True)


container_hidden_elements = Container(
    widgets=[
        progress_bar,
        note_box_license_1, note_box_license_2,
        done_text_download,
    ],
    direction="vertical",
    # gap=0
)


if g.YT_API_KEY is None:
    text_source_info.text = 'YouTube API key should be loaded manually'
    input_yt_API_KEY.show()
    container_input = Container(
        widgets=[
            input_yt_link,
            input_yt_API_KEY
        ],
        direction="horizontal",
        fractions=[3,1],    
    )
else:
    text_source_info.text = 'YouTube API key is loaded from the team files.'
    input_yt_API_KEY.hide()
    container_input = Container(
        widgets=[input_yt_link]
    )

text_connection_status.hide()

card_1 = Card(
    title="Pull video from Youtube",
    content=Container(widgets=[ 
        container_input,
        field_available_licenses,
        text_source_info,
        text_connection_status,
        field_meta,
        container_buttons,
        container_hidden_elements,
    ]),
)


# card 1 states
# note_box_license_1.hide()
# note_box_license_2.hide()
# progress_bar.hide()
button_stop_download.hide()
# done_text_download.hide()

container_hidden_elements.hide()

card_2.lock(message='Please download video first')
card_3.lock(message='Please download video first')


@button_download.click
def download_video():

    # check statuses
    if input_yt_link.get_value()=="":
        raise RuntimeError('Please input YouTube link.')
    if input_yt_API_KEY.get_value()=="" \
        and g.YT_API_KEY==None:
        raise RuntimeError('Please input your API key.')

    if g.YT_API_KEY is None:
        g.YT_API_KEY = input_yt_API_KEY.get_value()
    # checking connection
    response = check_connection()
    text_connection_status.status = response[0]
    text_connection_status.text = response[1]
    text_connection_status.show()

    global is_stopped
    is_stopped = False

    progress_bar.hide()
    done_text_download.hide()
    container_hidden_elements.show()

    link = input_yt_link.get_value()
    yt_video_id = get_youtube_id(link)

    g.YT_VIDEO_ID = str(yt_video_id)


    meta_dict_2save = {
        'license_type' : True,
        'is_licensed_content' : True,
        'duration' : False,
        'author' : checkbox_author.is_checked(),
        'description' : checkbox_description.is_checked(),
        'title' : checkbox_title.is_checked(),
    }

    full_meta_dict = get_meta(yt_video_id, note_box_license_1, note_box_license_2)
    meta_dict_2save = {key: value for key, value in full_meta_dict.items() if meta_dict_2save[key]}

    meta_dict_2save['youtube_link'] = input_yt_link.get_value()
    meta_dict_2save['youtube_id'] = yt_video_id

    # g.YT_VIDEO_LINK = input_yt_link.get_value()
    # video_player._url = input_yt_link.get_value()
    g.META_DICT = json.dumps(meta_dict_2save)

    filename = os.path.join(os.getcwd(), f"src/videos/{yt_video_id}.mp4")

    if os.path.exists(filename):
        done_text_download.text = f'Video "{full_meta_dict["title"]}" was already downloaded.'
        done_text_download.status = 'success'
        done_text_download.show()
        # card_2.unlock()
    else:
        print('Getting Video...')   
        
        if not note_box_license_1.description == None:
            note_box_license_1.show()
        if not note_box_license_2.description == None:
            note_box_license_2.show()
        
        progress_bar.show()
        button_stop_download.show()

        with progress_bar(message=f"Downloading video...", total=100) as pbar:
            try:
                yt = YouTube(
                    f"https://www.youtube.com/watch?v={yt_video_id}"#, on_progress_callback=progress
                )
                stream = yt.streams.get_highest_resolution()
                filesize = stream.filesize

                with open(filename, 'wb') as f:
                    stream = request.stream(stream.url) # get an iterable stream
                    downloaded = 0

                    while True:
                        if is_stopped:
                            print('Download cancelled')
                            stream.close()
                            f.close(),
                            os.remove(filename)

                            button_stop_download.hide()
                            done_text_download.text = 'Video download was stopped.'
                            done_text_download.status = 'warning'
                            done_text_download.show()
                            return None
                            # break
                        chunk = next(stream, None) # get next chunk of video
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            pbar.update(
                                int(downloaded * 100 / filesize)
                            )     
                        else:
                            print("Video downloaded successfully!")
                            stream.close()
                            break
            except Exception as e:
                print("An error occurred while downloading the video:", e)
                exit()

            
        button_stop_download.hide()
        done_text_download.text = f'Video "{full_meta_dict["title"]}" was succesfully downloaded.'
        done_text_download.status = 'success'
        done_text_download.show()
        print('Video downloaded to directory:', os.path.join(os.getcwd(), f'src/videos/{yt_video_id}.mp4'))

    video_player.set_video(
        # os.path.join(os.getcwd(), f'src/videos/{yt_video_id}.mp4')
        f'static/{yt_video_id}.mp4'
    )

    match = re.match('PT(\d+H)?(\d+M)?(\d+S)?', full_meta_dict['duration']).groups()
    
    input_max_hours.max = int(match[0][:-1]) if match[0] else 0
    input_max_hours.value = int(match[0][:-1]) if match[0] else 0
    
    input_max_minutes.max = int(match[1][:-1]) if match[1] else 0
    input_max_minutes.value = int(match[1][:-1]) if match[1] else 0
    
    input_max_seconds.max = int(match[2][:-1]) if match[2] else 0
    input_max_seconds.value = int(match[2][:-1]) if match[2] else 0

    
    card_2.unlock()


@button_stop_download.click
def stop_download():

    global is_stopped
    is_stopped = True
