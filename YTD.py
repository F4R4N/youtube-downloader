#!usr/bin/dev python
import argparse
import sys
from pathlib import Path
from datetime import timedelta
from pynotifier import Notification
from pytube import YouTube, Playlist, exceptions
from pytube.cli import on_progress
import pytube
import pytube.request
from win10toast import ToastNotifier
# chunk size
pytube.request.default_range_size = 1048576  # 1MB

# TODO: test

USER_DOWNLOAD_PATH = Path.home() / "Downloads" / "YTD"
LINE = "\n" + "-" * 50

def home_path_creator():
    Path.mkdir(USER_DOWNLOAD_PATH, parents=True, exist_ok=True)


parser = argparse.ArgumentParser(prog='python YTD.py ', epilog='Download : python YTD.py -u <url> -d [360, 480, 720]'
                                                               ' -p empty or /path/to/dist\nVideo details : python '
                                                               'YTD.py -u <url> -v', add_help=False)
parser.add_argument('-u', '--url', help='Enter youtube video url[Required]', required=True)
parser.add_argument('-d', '--download', choices=['360p', '480p', '720p'], help='downloading the video with the given quality')
parser.add_argument('-v', '--verbose', help='give you information about video', action='store_true')
parser.add_argument('-p', '--path', default=USER_DOWNLOAD_PATH,
                    help='Path to download the video (leave empty to download to default path ~/Downloads/YTD)')
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')
parser.add_argument('-l', '--playlist', help='Download Youtube playlist.', action="store_true")
args = parser.parse_args()


def download_path_validator(path):
    download_path = Path(path)
    if not download_path.is_dir():
        print(f"No such directory: '{path}'")
        sys.exit(0)


def notify(title: str):
    notification_title = f"Downloading video '{title}' finished!"
    description = f"Youtube downloader downloaded '{title}' finished!"
    if sys.platform.startswith('linux'):
        Notification(title=notification_title, description=description, duration=10,
                     icon_path='favicon.ico', urgency="normal",).send()
    elif sys.platform.startswith('win32'):
        toast = ToastNotifier()
        toast.show_toast(title=title, msg=description, duration=10,
                         icon_path='favicon.ico')


def video_details(connection: YouTube):
    vid_length = str(timedelta(seconds=connection.length))
    details = LINE + f"\nVideo Title: {connection.title}\nVideo Author: {connection.author}\n" \
            f"Video Description: {connection.description}\nVideo Rate: {connection.rating}"\
            f"\nVideo Views: {connection.views}\nVideo Thumbnail Url: {connection.thumbnail_url}"\
            f"\nVideo Length: {vid_length}\n"+ LINE
    print(details)


def playlist_details(connection: Playlist):
    details = LINE + f"\nPlaylist Title: {connection.title}\nPlaylist Owner: {connection.owner}\n"\
            f"Playlist Description: {connection.description}\nPlaylist Views: {connection.views}\n"\
            f"Playlist has {connection.length} video(s) in it!"
    print(details)


def verbose_without_download(connection):
    if args.download is None:
        if args.playlist:
            playlist_details(connection=connection)
        else:
            video_details(connection=connection)
        sys.exit(0)


def download_video(video_url: str, resolution: str, path_to_save: str):
    try:
        youtube_video = YouTube(video_url, on_progress_callback=on_progress)
    except exceptions.RegexMatchError:
        print("ERROR: Wrong url pattern, make sure to copy the youtube video url or add '--playlist' if thats the case!")
        sys.exit(0)
    verbose_without_download(youtube_video)
    if args.verbose:
        video_details(youtube_video)
    print("Press Ctrl+c any time to stop downloading.")
    print(f"\nDownloading video '{youtube_video.title}' ...")
    video = youtube_video.streams.filter(res=resolution, file_extension="mp4").first()
    video.download(path_to_save)
    print("Finished!")
    print(f"'{youtube_video.title}' saved to '{path_to_save}'")
    notify(title=youtube_video.title)


def main(resolution: str, path_to_save: str):
    home_path_creator()
    download_path_validator(path_to_save)
    if args.playlist:
        youtube_playlist = Playlist(args.url)
        path = Path(path_to_save) / youtube_playlist.title
        Path.mkdir(path, exist_ok=True)
        if args.verbose:
            playlist_details(youtube_playlist)
        print(f"\nPlaylist '{youtube_playlist.title}' ...")
        print(LINE)
        for video_url in youtube_playlist.video_urls:
            download_video(video_url=video_url, resolution=resolution, path_to_save=path)

    else:
        download_video(video_url=args.url, resolution=resolution, path_to_save=path_to_save)
    print("Done!")


if __name__ == "__main__":
    try:
        main(resolution=args.download, path_to_save=args.path)
    except KeyboardInterrupt:
        print("Program has stopped by user!")
        sys.exit(0)
 