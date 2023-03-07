import os, json

from supervisely.app.widgets import (
    Button, Input, Checkbox, Container, Card,
    Empty,  Text, NotificationBox, Progress
)

from src.ui.trim import (
    card_2, input_min_seconds, input_max_seconds
)
from src.ui.settings import card_3

from src.utils import get_youtube_id, get_meta
from pytube import YouTube, request


input_text = Input(placeholder="Please input a link to your video in format 'https://www.youtube.com/...'")

text_meta = Text(text='Add meta')

checkbox_title = Checkbox(content="Title")
checkbox_description = Checkbox(content="Description")
checkbox_author = Checkbox(content="Author", checked=True)
checkbox_author.disable()


container_meta = Container(
    widgets=[
        checkbox_title,
        checkbox_description,
        checkbox_author,
        Empty()
    ],
    direction="horizontal",
    fractions=[.7,1,1,4]
)

text_notrim = Text('Optional')
checkbox_notrim = Checkbox('Do not trim the video')


button_download = Button(text="Download")


done_text_download = Text()


note_box_license = NotificationBox(
    title="Notice of Potential License Infringement!",
    box_type="warning",
)

progress_bar = Progress(message="My progress message", show_percents=True)
button_stop_download = Button(text="Stop")

container_hidden_elements = Container(
    widgets=[
        note_box_license, 
        progress_bar, button_stop_download,
        done_text_download
    ],
    direction="vertical",
    gap=3
)


card_1 = Card(
    title="Pull video from Youtube",
    content=Container(widgets=[
        input_text, 
        text_meta,
        container_meta,
        text_notrim,
        checkbox_notrim, 
        button_download,
        container_hidden_elements,
    ]),
)

# card 1
os.environ['is_notrim'] = str(int(checkbox_notrim.is_checked()))
note_box_license.hide()
progress_bar.hide()
button_stop_download.hide()
done_text_download.hide()

card_2.lock(message='You need to download video first')
card_3.lock(message='You need to download video first')

@checkbox_notrim.value_changed
def notrim(value):
    if value == True:
        card_2.lock(message='Choosed not to trim the video')
        os.environ['is_notrim'] = str(int(value))
    else:
        card_2.unlock()
        os.environ['is_notrim'] = str(int(value))


@button_download.click
def download_video():

    global is_stopped
    is_stopped = False

    progress_bar.hide()
    done_text_download.hide()

    link = input_text.get_value()
    yt_video_id = get_youtube_id(link)

    os.environ['yt_video_id'] = str(yt_video_id)

    checkbox_dict = {
        'duration_sec' : False,
        'author' : checkbox_author.is_checked(),
        'description' : checkbox_description.is_checked(),
        'title' : checkbox_title.is_checked(),
    }

    meta_dict = get_meta(yt_video_id, note_box_license)

    os.environ['meta_dict'] = json.dumps(
        {key: value for key, value in meta_dict.items() if checkbox_dict[key]}
    )
    if not note_box_license.description == None:
        note_box_license.show()

    print('Getting Video...')
    progress_bar.show()
    button_stop_download.show()
    with progress_bar(message=f"Downloading video...", total=100) as pbar:
        try:
            yt = YouTube(
                f"https://www.youtube.com/watch?v={yt_video_id}"#, on_progress_callback=progress
            )
            stream = yt.streams.get_highest_resolution()
            filesize = stream.filesize
            filename = os.path.join(os.getcwd(), f"src/videos/{yt_video_id}.mp4")

            with open(filename, 'wb') as f:
                stream = request.stream(stream.url) # get an iterable stream
                downloaded = 0

                while True:
                    if is_stopped:
                        # progress['text'] = 'Download cancelled'
                        print('Download cancelled')
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

        
    print('Video downloaded to directory:', os.path.join(os.getcwd(), f'src/videos/{yt_video_id}.mp4'))


    if is_stopped:
        button_stop_download.hide()
        done_text_download.text = 'Video download was stopped.'
        done_text_download.status = 'warning'
        done_text_download.show()
    else:
        button_stop_download.hide()
        done_text_download.text = f'Video "{meta_dict["title"]}" was succesfully downloaded.'
        done_text_download.status = 'success'
        done_text_download.show()


    input_min_seconds.min = 0
    input_min_seconds.value = 0
    input_max_seconds.max = meta_dict['duration_sec']
    input_max_seconds.value = meta_dict['duration_sec']


    card_2.lock('Selected not to trim the video') if bool(int(os.environ['is_notrim'])) else card_2.unlock()
    card_3.unlock()

    os.environ['download_status'] = done_text_download.status


@button_stop_download.click
def stop_download():

    global is_stopped
    is_stopped = True

