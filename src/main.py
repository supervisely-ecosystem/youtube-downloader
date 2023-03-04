"""
- текстовый инпут для ссылки на видео
- селектор типа лицензии - Public domain, Creative Commons, Copyleft
- виджет для выбора интервала(начало, конец) видео для скачивания
- галочками ставишь, какую ещё информацию о видео нужно скачать вместе 
с видео (title, description, author, etc) и сохраняешь это в мета-данные видео
прогресс скачивания с возможностью остановить загрузку
- возможность указывать destination - новый проект/датасет или существующий
приложение не завершается само. Его можно остановить только вручную
"""
import os, json

import supervisely as sly
from dotenv import load_dotenv

from supervisely.app.widgets import Card, Container

from src.ui.download import button_download, input_text, button_download, buttons_container_1, note_box_license, progress_bar, button_stop_download, done_text
from src.ui.download import checkbox_title, checkbox_description, checkbox_author

from src.ui.trim import button_trim, buttons_container_2, done_label_trim, input_min_seconds, input_max_seconds

from src.ui.settings import button_api_upload, select_destination, buttons_container_3, trimmed_video_thumbnail 
from src.ui.settings import input_project_id, input_dataset_id

from src.utils import get_youtube_id, trim, get_meta
from pytube import YouTube, request

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()


card_1 = Card(
    title="Pull video from Youtube",
    content=Container(widgets=[
    input_text, 
    buttons_container_1, 
    note_box_license, 
    progress_bar, button_stop_download,
    done_text
    ]),
)

note_box_license.hide()
progress_bar.hide()
button_stop_download.hide()
done_text.hide()



card_2 = Card(
    title="Trim video",
    content=Container(widgets=[
    buttons_container_2, done_label_trim
    ]),
)
done_label_trim.hide()



card_3 = Card(
    title="Push to supervisely",
    content=Container(widgets=[
    buttons_container_3, trimmed_video_thumbnail 
    ]),
)
trimmed_video_thumbnail.hide()


@button_download.click
def download_video():

    progress_bar.hide()
    done_text.hide()

    link = input_text.get_value()
    yt_video_id = get_youtube_id(link)

    checkbox_dict = {
        'author' : checkbox_author.is_checked(),
        'description' : checkbox_description.is_checked(),
        'title' : checkbox_title.is_checked(),
    }
    os.environ['meta_dict'] = json.dumps(
        get_meta(yt_video_id, checkbox_dict, note_box_license)
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
                # is_cancelled = False
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

    os.environ['yt_video_id'] = str(yt_video_id)

    if is_stopped:
        button_stop_download.hide()
        done_text.text = 'Video download was stopped.'
        done_text.status = 'warning'
        done_text.show()
    else:
        button_stop_download.hide()
        done_text.text = 'YouTube video was succesfully downloaded.'
        done_text.status = 'success'
        done_text.show()


is_stopped = False

@button_stop_download.click
def stop_download():

    global is_stopped
    is_stopped = True

@button_trim.click
def trim_video():

    done_label_trim.hide()

    start_time = input_min_seconds.get_value()
    end_time = input_max_seconds.get_value()

    yt_video_id = os.environ['yt_video_id']

    input_path = os.path.join(
        os.getcwd(), f'src/videos/{yt_video_id}.mp4'
    )
    output_path = os.path.join(
        os.getcwd(), f'src/videos/trimmed_{yt_video_id}.mp4'
    )

    trim(
        input_path=input_path,
        output_path=output_path,
        start=start_time,
        end=end_time
    )

    done_label_trim.show()
 

# input_dataset_id.hide()

@select_destination.value_changed
def sel_dest(value):
    if value == 'new':
        input_project_id.disable()
        input_dataset_id.disable()
    else:
        input_project_id.enable()
        input_dataset_id.enable()

@button_api_upload.click
def upload():

    destination = select_destination.get_value()

    if destination == 'current':
        
        project_id = input_project_id.get_value()
        dataset_id = input_dataset_id.get_value()

    if destination == 'new':

        workspace_id = sly.env.workspace_id()

        project = api.project.create(
            workspace_id, "YouTube Video Downloader", 
            type=sly.ProjectType.VIDEOS, 
            change_name_if_conflict=True
        )

        dataset = api.dataset.create(project.id, "YT_video")

        project_id = project.id
        dataset_id = dataset.id

    yt_video_id = os.environ['yt_video_id']
    video_name = f"trimmed_{yt_video_id}.mp4"
    video_path = os.path.join(
        os.getcwd(), f'src/videos/trimmed_{yt_video_id}.mp4'
    )
   
    print(f"Project ID: {project_id}")
    print(f"Dataset ID: {dataset_id}")

    meta_dict = json.loads(os.environ['meta_dict'])
 
    video = api.video.upload_path(
        dataset_id,
        name=video_name,
        path=video_path,
        meta=meta_dict
    )

    print(f'Video "{video.name}" uploaded to Supervisely with ID:{video.id}')

    video_info = api.video.get_info_by_id(id=video.id)

    trimmed_video_thumbnail.set_video(video_info)
    trimmed_video_thumbnail.show()


layout = Container(widgets=[card_1, card_2, card_3], direction="vertical")
app = sly.Application(layout=layout)
