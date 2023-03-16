import os, json, re
import src.globals as g

from supervisely.app.widgets import (
    Button, Input, Checkbox, Container, 
    Card, Empty, Field
)

from src.ui._common_widgets import (
    container_hidden_elements, text_check_input_ytlink,
    done_text_download, progress_bar,
    note_box_license_1, note_box_license_2, video_player, 
    slider, field_slider, trimming_range_float
)

from src.ui.trim import card_2
from src.ui.upload import card_3

from src.utils import (
    get_youtube_id, get_meta
)
from pytube import YouTube, request

input_yt_link = Input(
    placeholder="Please input a link to your video in format 'https://www.youtube.com/...'"
)


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
    fractions=[1,.8,5],
)


card_1 = Card(
    title="Pull video from Youtube",
    content=Container(widgets=[ 
        input_yt_link,
        text_check_input_ytlink,
        field_available_licenses,
        field_meta,
        container_buttons,
        container_hidden_elements,
    ]),
)

# card 1 states
button_stop_download.hide()
text_check_input_ytlink.hide()
container_hidden_elements.hide()

card_2.lock(message='Please download video first')
card_3.lock(message='Please download video first')


@button_download.click
def download_video():

    global is_stopped
    is_stopped = False

    # check statuses
    if input_yt_link.get_value()=="":
        text_check_input_ytlink.text = 'Input form is empty. Please input YouTube link.'
        text_check_input_ytlink.status = 'error'
        text_check_input_ytlink.show()
        return None
    if not input_yt_link.get_value().startswith("https://www.youtube.com/"): 
        text_check_input_ytlink.text = "Invalid YouTube link. Please use desktop format of url starting with 'https://www.youtube.com/...'"
        text_check_input_ytlink.status = 'error'
        text_check_input_ytlink.show()
        return None
    else:
        text_check_input_ytlink.hide()

    progress_bar.hide()
    done_text_download.hide()
    note_box_license_1.hide()
    note_box_license_2.hide()
    container_hidden_elements.show()

    link = input_yt_link.get_value()
    yt_video_id = get_youtube_id(link)
    g.YT_VIDEO_ID = str(yt_video_id)

    meta_dict_2save = {
        'license_type' : True,
        'is_licensed_content' : True,
        'duration' : False,
        'duration_sec' : False,
        'author' : checkbox_author.is_checked(),
        'description' : checkbox_description.is_checked(),
        'title' : checkbox_title.is_checked(),
    }

    full_meta_dict = get_meta(yt_video_id, note_box_license_1, note_box_license_2)


    meta_dict_2save = {key: value for key, value in full_meta_dict.items() if meta_dict_2save[key]}

    meta_dict_2save['youtube_link'] = input_yt_link.get_value()
    meta_dict_2save['youtube_id'] = yt_video_id

    g.META_DICT = json.dumps(meta_dict_2save)

    if not note_box_license_1.description == None:
        note_box_license_1.show()
    if not note_box_license_2.description == None:
        note_box_license_2.show()

    filename = os.path.join(os.getcwd(), f"src/videos/{yt_video_id}.mp4")

    if os.path.exists(filename):
        done_text_download.text = f'Video "{full_meta_dict["title"]}" was already downloaded.'
        done_text_download.status = 'success'
        done_text_download.show()
        # card_2.unlock()
    else:
        print('Getting Video...')   

        if not os.path.exists('src/videos/'):
            os.makedirs('src/videos/')
        
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
        f'static/{yt_video_id}.mp4'
    )

    slider.set_min(0)
    slider.set_max(full_meta_dict['duration_sec'])
    slider.set_value([0, int(full_meta_dict['duration_sec']/5) ] )

    trimming_range_float['end'] = [int(full_meta_dict['duration_sec']/5)]
 

    field_slider._description = f"Video duration: {full_meta_dict['duration_sec']} seconds"
    field_slider.update_data()

    card_2.unlock()
    card_3.unlock()


@button_stop_download.click
def stop_download():

    global is_stopped
    is_stopped = True
