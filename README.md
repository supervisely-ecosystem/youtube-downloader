<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/115161827/226859998-b151fb10-9765-481d-a3d4-94819c9dea75.jpg"/>

# Download and trim videos from YouTube

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#Preparation">Preparation</a> •
  <a href="#How-To-Run">How To Run</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/dev-smart-tool-batched)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/dev-smart-tool-batched)
[![views](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/dev-smart-tool-batched&counter=views&label=views)](https://supervise.ly)
[![used by teams](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/dev-smart-tool-batched&counter=downloads&label=used%20by%20teams)](https://supervise.ly)
[![runs](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/dev-smart-tool-batched&counter=runs&label=runs&123)](https://supervise.ly)

</div>

## Overview
This app allows you to download and trim YouTube videos directly to your video editing project. After specifying the video URL, with only one click, you can download and trim the video and add it to your project. The trimmed videos will include metadata from YouTube, such as the title and description. Additionally, the app will notify you about possible license issues and video licenses.<br>
For example, you enter a link for a videoclip of a popular song, such as [this one](https://www.youtube.com/watch?v=dQw4w9WgXcQ), choose the available metadata, and click on "Download" (Don't forget to input your YouTube v3 API key, either manually or by importing a teamfile). After that, you can specify the trimming segment of the video (or leave it untouched) and push the video to the selected project and dataset (or create new ones). Once done, the video clip will be uploaded to the Supervisely dataset with all the necessary metadata. For more details, please refer to the [How To Run](#How-To-Run) section.<br>

## Preparation
To use this app, you need to obtain a YouTube v3 API key. To do so, you must have a Google account and follow the instructions provided by [YouTube](https://developers.google.com/youtube/v3/getting-started). There are two options for using your API key: you can store it in a .env file within the team files, or you can enter it directly in the app's GUI. We recommend using team files as it is more convenient and secure, but you may choose the option that best suits your needs.<br>

### Using team files
1. Create a .env file with the following content:<br>
```YT_API_KEY=<your_api_key>```<br>
2. Upload the .env file to the team files.<br>
3. Right-click on the .env file, select "Run app" and choose the "YouTube Downloader" app.<br>
The app will be launched with the API key from the .env file and you won't need to enter it manually.<br>

### Entering the API key manually
1. Launch the app.<br>
2. You will notice that all cards of the app are locked except the "YouTube API Token" card. Enter your API key in the field and press the `Check API key`.<br>
3. If the API key is valid, the Video settings card will be unlocked and you can proceed with using the app. If the API key is invalid, you will see an error message and will need to re-enter the API key.<br>
Now you can use the app. However, please note that in this case, you will need to enter the API key every time you launch the app.<br>

## How To Run
Note: in this section, we consider that you have already obtained the API key, and use it to run the app. If you haven't done it yet, see the [Preparation](#Preparation) section.<br>
So, here are the steps to download and trim video from YouTube:<br>

**Step 1:** Enter the copy-pasted YouTube link in the `"https://www.youtube.com/..."` format.<br><br>
**Step 2:** In the `Video Settings ` section, examine the `Available licenses` and indicate the type of metadata you wish to add (Title, Description, Author) in the `Add meta` field. Please note that for YouTube videos, there are only two types of available licenses: YouTube and Creative Commons. <br><br>
**Step 3:** After completing the previous steps, click the `Download` button and wait for the process to complete. You can stop the process at any time. <br><br>
**Step 4:** Indicate if you need to trim the video in the `Trim Settings` section. If so, specify the trimming time interval by selecting the timestamp in the video player and clicking the corresponding button. Alternatively, you can use the slider to choose the trimming segment and click the `Trim` button. <br><br>
**Step 5:** In the `Output Settings`, you can specify the project and dataset to which you would like to add the video. If you do not specify a project or dataset, one will be created automatically using the search query and the current date to generate names. Alternatively, you can specify custom names for the project or dataset manually. <br><br>
**Step 6:** After completing all of the previous steps, you can click the `Start Upload` button to begin uploading the video to the dataset. Once the upload is complete, the app will display a thumbnail of the video. You can click on the link to open the project in the video editor. <br><br>
