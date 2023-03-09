import os, json
import src.globals as g

from supervisely.app.widgets import (
    Button, Input, Checkbox, Container, Card,
    Empty,  Text, Progress, Field
)

from src.ui._common_widgets import (
    done_text_download, input_min_seconds, input_max_seconds,
    note_box_license_1, note_box_license_2
)

from src.ui.trim import card_2
from src.ui.upload import card_3

from src.utils import get_youtube_id, get_meta
from pytube import YouTube, request

input_yt_link = Input(placeholder="Please input a link to your video in format 'https://www.youtube.com/...'")

input_yt_API_KEY = Input(placeholder="Please input YouTube v3 API KEY")
# text_available_licenses = Text(text="Available licenses: 'youtube', 'creativeCommon'")

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
    fractions=[.7,1,1,4],
)


field_meta = Field(content=container_meta, title="Add meta")


button_download = Button(text="Download")
button_stop_download = Button(text="Stop")

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
    gap=3
)



if g.YT_API_KEY is None:
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
    input_yt_API_KEY.hide()
    container_input = Container(
        widgets=[input_yt_link]
    )

card_1 = Card(
    title="Pull video from Youtube",
    content=Container(widgets=[
        container_input,
        field_available_licenses,
        field_meta,
        container_buttons,
        container_hidden_elements,
    ]),
)


# card 1 states
note_box_license_1.hide()
note_box_license_2.hide()
progress_bar.hide()
button_stop_download.hide()
done_text_download.hide()

card_2.lock(message='Please download video first')
card_3.lock(message='Please download video first')


@button_download.click
def download_video():

    # check statuses
    if input_yt_link.get_value()=="":
        raise RuntimeError('Please input YouTube link.')
    if input_yt_API_KEY.get_value()=="":
        raise RuntimeError('Please input your API key.')

    if g.YT_API_KEY is None:
        g.YT_API_KEY = input_yt_API_KEY.get_value()

    global is_stopped
    is_stopped = False
    is_stopped_fixed = is_stopped

    progress_bar.hide()
    done_text_download.hide()

    link = input_yt_link.get_value()
    yt_video_id = get_youtube_id(link)

    g.YT_VIDEO_ID = str(yt_video_id)

    meta2save_dict = {
        'license_type' : True,
        'is_licensed_content' : True,
        'duration_sec' : False,
        'author' : checkbox_author.is_checked(),
        'description' : checkbox_description.is_checked(),
        'title' : checkbox_title.is_checked(),
    }

    meta_dict = get_meta(yt_video_id, note_box_license_1, note_box_license_2)

    g.META_DICT = json.dumps(
        {key: value for key, value in meta_dict.items() if meta2save_dict[key]}
    )

    if not os.path.exists('src/videos/'):
        os.makedirs('src/videos/')
    filename = os.path.join(os.getcwd(), f"src/videos/{yt_video_id}.mp4")

    if os.path.exists(filename):
        done_text_download.text = f'Video "{meta_dict["title"]}" was already downloaded.'
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
                            is_stopped_fixed = is_stopped
                            stream.close()
                            f.close(),
                            os.remove(filename)
                            break
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

            
    if is_stopped_fixed:
        button_stop_download.hide()
        done_text_download.text = 'Video download was stopped.'
        done_text_download.status = 'warning'
        done_text_download.show()
        return None
    else:
        button_stop_download.hide()
        done_text_download.text = f'Video "{meta_dict["title"]}" was succesfully downloaded.'
        done_text_download.status = 'success'
        done_text_download.show()
        print('Video downloaded to directory:', os.path.join(os.getcwd(), f'src/videos/{yt_video_id}.mp4'))



    input_min_seconds.min = 0
    input_min_seconds.value = 0
    input_max_seconds.max = meta_dict['duration_sec']
    input_max_seconds.value = meta_dict['duration_sec']


    card_2.unlock()



@button_stop_download.click
def stop_download():

    global is_stopped
    is_stopped = True

