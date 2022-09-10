#!usr/bin/dev python
import argparse
import sys
from pathlib import Path
from pynotifier import Notification
from pytube import YouTube
from pytube.cli import on_progress
from win10toast import ToastNotifier

# TODO: add playlist download
# TODO: check progressbar


def home_path_creator():
    user_download_path = Path.home() / "Downloads" / "YTD"
    Path.mkdir(user_download_path, parents=True, exist_ok=True)
    return user_download_path


parser = argparse.ArgumentParser(prog='python YTD.py ', epilog='Download : python YTD.py -u <url> -d [360, 480, 720]'
                                                               ' -p empty or /path/to/dist\nVideo details : python '
                                                               'YTD.py -u <url> -v', add_help=False)
parser.add_argument('-u', '--url', help='Enter youtube video url[Required]', required=True)
parser.add_argument('-d', '--download', choices=['360p', '480p', '720p'], help='downloading the video with the given quality')
parser.add_argument('-v', '--verbose', help='give you information about video', action='store_true')
parser.add_argument('-p', '--path', default=home_path_creator(),
                    help='path to download the video( leave empty to download to default path ~/Downloads/YTD )')
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')
args = parser.parse_args()


def download_path_validator(path):
    download_path = Path(path)
    if not download_path.is_dir():
        print(f"No such directory: '{path}'")
        exit()


def main():
    youtube_connect = YouTube(args.url, on_progress_callback=on_progress)

    if args.verbose:
        details(connection=youtube_connect)

    if args.download is None:
        details(connection=youtube_connect)
    else:
        download_path_validator(args.path)
        video_path = download(connection=youtube_connect, resolution=args.download, path_to_save=args.path)
        print(f"{youtube_connect.title} saved to {video_path}")


def download(connection: YouTube, resolution: str, path_to_save: str):
    print(f"Downloading '{connection.title}' ...")
    video = connection.streams.filter(res=resolution, file_extension="mp4").first()
    video.download(path_to_save)
    print("Finished!")
    notify()
    return path_to_save


def notify():
    if sys.platform.startswith('linux'):
        Notification(title="Download Finished", description="youtube downloader download finished", duration=6,
                     icon_path='favicon.ico', urgency=Notification.URGENCY_NORMAL).send()
    elif sys.platform.startswith('win32'):
        toast = ToastNotifier()
        toast.show_toast(title="Download Finished", msg="youtube downloader download finished", duration=6,
                         icon_path='favicon.ico')


def details(connection):
    vid_title = connection.title
    vid_author = connection.author
    vid_description = connection.description
    vid_rate = connection.rating
    vid_views = connection.views
    vid_photo = connection.thumbnail_url
    vid_caption = connection.captions
    vid_length = connection.length
    if vid_length >= 60:
        vid_length //= 60
        vid_length = str(vid_length) + " 'M"
    elif vid_length < 60:
        vid_length = str(vid_length) + " 'S"
    all_details = "\n\nVideo Title: {0}\nVideo Author: {1}\nVideo Description: {2}\nVideo Rate: {3}\nVideo Views:" \
                  " {4}\nVideo Thumbnail Url: {5}\nVideo Caption: {6}\nVideo Length: {7}".format(vid_title, vid_author,
                                                                                                 vid_description,
                                                                                                 vid_rate, vid_views,
                                                                                                 vid_photo, vid_caption,
                                                                                                 vid_length)
    print(all_details)


if __name__ == "__main__":
    main()
