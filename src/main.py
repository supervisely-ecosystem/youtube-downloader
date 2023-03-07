import os, json

import supervisely as sly
from dotenv import load_dotenv

from supervisely.app.widgets import Container

from src.ui.download import (
    card_1, checkbox_notrim, button_download, input_text, button_download,
    note_box_license, progress_bar, 
    button_stop_download, done_text_download,
    checkbox_title, checkbox_description, checkbox_author
)

from src.ui.trim import (
    card_2, button_trim, done_text_trim,
    input_min_seconds, input_max_seconds
)

from src.ui.settings import (
    card_3, button_api_upload, select_destination, 
    trimmed_video_thumbnail, select_project, select_dataset,
    checkbox_new_destination
)

from src.utils import get_youtube_id, trim, get_meta
from pytube import YouTube, request


# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))


api = sly.Api()

card_2.lock(message='You need to download video first')
card_3.lock(message='You need to download video first')

# card 1
os.environ['is_notrim'] = str(int(checkbox_notrim.is_checked()))
note_box_license.hide()
progress_bar.hide()
button_stop_download.hide()
done_text_download.hide()

# card 2
# input_min_seconds.disable()
# input_max_seconds.disable()
done_text_trim.hide()

# card 3
trimmed_video_thumbnail.hide()


@checkbox_notrim.value_changed
def notrim(value):
    # if value == 'new':
    if value == True:
        card_2.lock(message='Choosed not to trim the video')
        os.environ['is_notrim'] = str(int(value))
        # card_3.unlock() if 
    else:
        card_2.unlock()
        os.environ['is_notrim'] = str(int(value))
        # card_3.lock()
 

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

    # input_min_seconds.enable()
    # input_max_seconds.enable()

    card_2.lock('Choosed not to trim the video') if bool(int(os.environ['is_notrim'])) else card_2.unlock()
    card_3.unlock()


@button_stop_download.click
def stop_download():

    global is_stopped
    is_stopped = True


@button_trim.click
def trim_video():

    done_text_trim.hide()

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

    
    done_text_trim.status = 'success'
    done_text_trim.show()
    card_3.unlock()
    # checkbox_notrim.disable()
 

# @select_destination.value_changed
@checkbox_new_destination.value_changed
def sel_dest(value):
    # if value == 'new':
    if value == True:
        select_project.disable()
        select_dataset.disable()
    else:
        select_project.enable()
        select_dataset.enable()

@button_api_upload.click
def upload():

    # Checking statuses
    if not done_text_download.status == 'success':
        raise RuntimeError('Video was not successfully downloaded.')
    if (not done_text_trim.status == 'success')\
        and (not bool(int(os.environ['is_notrim']))):
        raise RuntimeError('Video was not successfully trimmed.')

    new_destination = checkbox_new_destination.is_checked()

    # if destination == 'current':
    if not new_destination:

        if select_project.get_selected_id() == None:
            raise RuntimeError('Please specify your project.')
        else:
            project_id = select_project.get_selected_id()

        if select_dataset.get_selected_id() == None:
            raise RuntimeError('Please specify your dataset.')
        else:
            dataset_id = select_dataset.get_selected_id()
            
 
    # elif destination == 'new':
    elif new_destination:

        workspace_id = sly.env.workspace_id()

        project = api.project.create(
            workspace_id, "YouTube Video Downloader", 
            type=sly.ProjectType.VIDEOS, 
            change_name_if_conflict=True
        )

        dataset = api.dataset.create(project.id, "YT_video")

        project_id = project.id
        dataset_id = dataset.id

    else:
        raise ValueError(f'Unknown error with value "{new_destination}"')


    yt_video_id = os.environ['yt_video_id']

    if bool(int( os.environ['is_notrim'] )):
        video_name = f"{yt_video_id}.mp4"
    else:
        video_name = f"trimmed_{yt_video_id}.mp4"

    video_path = os.path.join(
        os.getcwd(),
        f'src/videos/{video_name}'
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

    video_info = api.video.get_info_by_id(id=video.id)

    trimmed_video_thumbnail.set_video(video_info)
    trimmed_video_thumbnail.show()

    print(f'Video "{video.name}" uploaded to Supervisely with ID:{video.id}')


layout = Container(widgets=[card_1, card_2, card_3], direction="vertical")
app = sly.Application(layout=layout)

