# def progress_function(stream, chunk, bytes_remaining):
#     total_size = stream.filesize
#     bytes_downloaded = total_size - bytes_remaining
#     percent_complete = bytes_downloaded / total_size * 100
#     print(f"{percent_complete:.2f}% downloaded")
    
from pytube import YouTube
import sys

def progress_callback(stream, chunk, bytes_remaining):
    # Calculate the percentage of the file that has been downloaded
    percent = (100 * (stream.filesize - bytes_remaining)) / stream.filesize
    # Create a progress bar with '=' characters for completed chunks and '-' characters for incomplete chunks
    progress_bar = '[' + '=' * int(percent / 2) + '-' * int((100 - percent) / 2) + ']'
    # Print the progress bar and the percentage of completion
    sys.stdout.write('\r' + progress_bar + ' {:.2f}%'.format(percent))
    sys.stdout.flush()
    
def download_video(link):

    yt = YouTube(link, on_progress_callback=progress_callback)

    # Select the highest resolution available
    stream = yt.streams.get_highest_resolution()

    # Download the video and update the progress bar
    stream.download(filename='my_video2.mp4')

# Example usage
# download_video('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
download_video('https://www.youtube.com/watch?v=Pcz3OJVhfhs')
print('Dwn!')
