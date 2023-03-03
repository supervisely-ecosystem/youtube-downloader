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
import os

import supervisely as sly
from dotenv import load_dotenv

from supervisely.app.widgets import Button, Card, Container, Progress, VideoThumbnail
from src.widgets import buttons_container_1, buttons_container_2, input_text, button_download, button_trim, button_api_upload

from src.widgets import done_label_download, done_label_trim, done_label_upload, select_destination
from src.widgets import input_min_seconds, input_max_seconds
from src.utils import get_video, trim

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()

# %%
card_1 = Card(
    title="Pull video from Youtube",
    content=Container(widgets=[input_text, buttons_container_1, done_label_download]),
)

progress_bar = Progress(message="My progress message", show_percents=True)

done_label_download.hide()

card_1_ = Card(
    title="Progress",
    content=Container(widgets=[progress_bar], ),
)

# initialize widgets we will use in UI
video_thumbnail = VideoThumbnail()

card_2 = Card(
    title="Trim video",
    content=Container(widgets=[buttons_container_2, done_label_trim]),
)

done_label_trim.hide()

trimmed_video_thumbnail = VideoThumbnail()

card_3 = Card(
    title="Push to supervisely",
    content=Container(widgets=[button_api_upload, select_destination, done_label_upload, trimmed_video_thumbnail ]),
)

done_label_upload.hide()
trimmed_video_thumbnail.hide()
# %%
# def get_workspace():

# %%

@button_download.click
def download_video():

    done_label_download.hide()

    link = input_text.get_value()

    print('Getting Video...')
    yt_video_id = get_video(link)

    print(os.path.join(os.getcwd(), f'src/videos/{yt_video_id}.mp4'))

    os.environ['yt_video_id'] = str(yt_video_id)

    done_label_download.show()


@button_trim.click
def trim_video():

    done_label_trim.hide()

    start_time = input_min_seconds.get_value()
    end_time = input_max_seconds.get_value()

    input_path = os.path.join(
        os.getcwd(),'src/videos/', (os.environ['yt_video_id']+'.mp4')
    )
    output_path = os.path.join(
        os.getcwd(), 'src/videos/', ('trimmed_' + os.environ['yt_video_id'] + '.mp4')
    )

    trim(
        input_path=input_path,
        output_path=output_path,
        start=start_time,
        end=end_time
    )

    done_label_trim.show()
 

@button_api_upload.click
def upload():
    done_label_upload.hide()

    workspace_id = sly.env.workspace_id()

    project = api.project.create(
        workspace_id, "YTvideos", 
        type=sly.ProjectType.VIDEOS, 
        change_name_if_conflict=True
    )

    print(f"Project ID: {project.id}")

    dataset = api.dataset.create(project.id, "YTvideo")
    print(f"Dataset ID: {dataset.id}")

    video_name = "trimmed_" + os.environ['yt_video_id'] + ".mp4"
    video_path = os.path.join(os.getcwd(),'src/videos/',('trimmed_' + os.environ['yt_video_id'] + '.mp4'))


    video = api.video.upload_path(
        dataset.id,
        name=video_name, 
        path=video_path
    )

    print(f'Video "{video.name}" uploaded to Supervisely with ID:{video.id}')

    video_info = api.video.get_info_by_id(id=video.id)

    trimmed_video_thumbnail
    # trimmed_video_thumbnail.set_video(video_info)

layout = Container(widgets=[card_1, card_2, card_3], direction="vertical")
app = sly.Application(layout=layout)
