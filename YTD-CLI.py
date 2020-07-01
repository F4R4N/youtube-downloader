#!usr/bin/dev python
from pytube import YouTube
import os, sys
from win10toast import ToastNotifier
from pynotifier import Notification
import argparse

# color table
ENDC = '\033[0m'
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
CYAN = '\033[96m'
YELLOW = '\033[93m'

# required=True

parser = argparse.ArgumentParser(prog='python YTD.py ', epilog='Download : python YTD.py -u <url> -d [360, 480, 720]'
                                                               ' -p empty or /path/to/dist\nVideo details : python '
                                                               'YTD.py -u <url> -v', add_help=False)
parser.add_argument('-u', '--url', help='enter youtube video url', )
parser.add_argument('-d', '--download', choices=['360', '480', '720'], help='downloading the video with the given quaity')
parser.add_argument('-v', '--verbose', help='give you information about video', action='store_true')
parser.add_argument('-p', '--path', nargs='*',
                    help='path to download the video( leave empty to download to defualt path ~/Downloads/YTD )')
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')
args = parser.parse_args()

dl = os.path.expanduser('~/Downloads')
try:
    os.mkdir('YTD')
except FileExistsError:
    ytd_path = os.path.join(dl, 'YTD')


def main_menu():
    # print(args.path)
    if args.url is not None:
        url_input = args.url
        global youtube_connect
        youtube_connect = YouTube(url_input)

    if not len(sys.argv) > 1:
        parser.print_help()

    if args.download is not None and args.path is None and args.path is None:
        parser.error('[ -d | --download ] require [ -p | --path ] put it empty to download to default path')

    if args.verbose and args.url is None:
        parser.error('[ -v | --verbose ] require the video url add [ -u | --url ] <url>')
    # if args.download is None:
    # details()
    if args.verbose:
        details()
    if args.url is not None and args.download is None:
        details()

    elif args.url is not None and args.download is not None:
        if args.download == '360':
            path = args.path
            stream_360 = youtube_connect.streams.filter(res='360p').first()
            if path is None or not [] or not '':
                path = ytd_path
            stream_360.download(path)
            notify()
        elif args.download == '480':
            stream_480 = youtube_connect.streams.filter(res='480p').first()
            path = args.path
            if path == '' or None:
                path = ytd_path
            else:
                path = path
            stream_480.download(path)
            notify()
        elif args.download == '720':
            stream_720 = youtube_connect.streams.filter(res='720p').first()
            path = args.path
            if path == '' or None:
                path = ytd_path
            else:
                path = path
            stream_720.download(path)
            notify()


def notify():
    if sys.platform.startswith('linux'):
        Notification(title="Download Finished", description="youtube downloader download finished", duration=6,
                     icon_path='favicon.ico', urgency=Notification.URGENCY_NORMAL).send()
    elif sys.platform.startswith('win32'):
        toast = ToastNotifier()
        toast.show_toast(title="Download Finished", msg="youtube downloader download finished", duration=6,
                         icon_path='favicon.ico')


def details():
    vid_title = youtube_connect.title
    vid_author = youtube_connect.author
    vid_description = youtube_connect.description
    vid_rate = youtube_connect.rating
    vid_views = youtube_connect.views
    vid_photo = youtube_connect.thumbnail_url
    vid_caption = youtube_connect.captions
    if vid_caption == '' or vid_caption is None or vid_caption == {}:
        vid_caption = "video has no caption"
    vid_length = youtube_connect.length
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
    main_menu()
