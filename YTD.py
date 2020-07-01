#!usr/bin/dev python
from pytube import YouTube
import os, sys
from win10toast import ToastNotifier
from pynotifier import Notification
# color table
ENDC = '\033[0m'
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
CYAN = '\033[96m'
YELLOW = '\033[93m'

dl = os.path.expanduser('~/Downloads')
try:
	os.mkdir('YTD')
except FileExistsError:
    ytd_path = os.path.join(dl, 'YTD')

def main_menu():

    while True:
        global url_input
        url_input = input(f"\n{BLUE}Note: Control + C any time to cancel download{ENDC}\n{GREEN}enter video url {ENDC}: ")
 
        try:
            global youtube_connect
            youtube_connect = YouTube(url_input)
            details()
            menu_input = int(input("\n\n1.Download\n2.enter new url\n3.Exit\n: "))
            if menu_input == 1:
                download()
            elif menu_input == 2:
                main_menu()
            elif menu_input == 3:
                print("bye")
                exit()
            else:
                print("input not found !!")
        except TypeError:
            print(f"{RED}invalid entry !! \nerror: type error{ENDC}")
            break
        
def notify():
    if sys.platform.startswith('linux'):
        Notification(title="Download Finished", description="youtube downloader download finished", duration=6, icon_path='favicon.ico',urgency=Notification.URGENCY_NORMAL).send()
    elif sys.platform.startswith('win32'):
        toast = ToastNotifier()
        toast.show_toast(title="Download Finished", msg="youtube downloader download finished", duration=6, icon_path='favicon.ico')

def download():
    while True:
        try:
            video_quality = int(input("\n1.360p\n2.480p\n3.720p\n4.main menu\n: "))

            if video_quality == 1:
                path = input("enter exact path for file to save, or leave empty to download to defualt path(~/Downloads/YTD) : ")
                print("press Ctrl+c to cancel download any time")
                stream_360 = youtube_connect.streams.filter(res='360p').first()
                if path == '' or None:
                    path = ytd_path
                else:
                    path = path
                stream_360.download(path)
                notify()
            elif video_quality == 2:
                stream_480 = youtube_connect.streams.filter(res='480p').first()
                path = input("enter exact path for file to save, or leave empty to download to defualt path(~/Downloads/YTD) : ")
                print("press Ctrl+c to cancel download any time")
                if path == '' or None:
                    path = ytd_path
                else:
                    path = path
                stream_480.download(path)
                notify()

            elif video_quality == 3:
                stream_720 = youtube_connect.streams.filter(res='720p').first()
                path = input("enter exact path for file to save, or leave empty to download to defualt path(~/Downloads/YTD) : ")
                print("press Ctrl+c to cancel download any time")
                if path == '' or None:
                    path = ytd_path
                else:
                    path = path
                stream_720.download(path)
                notify()

            elif video_quality == 4:
                main_menu()
            else:
                print(f"{RED}invalid entry{ENDC} ")
                download()
        except Exception:
            print(f"{YELLOW}something goes wrong check your internet and try again later !!!{ENDC}")

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
    all_details = "\n\nVideo Title: {0}\nVideo Author: {1}\nVideo Description: {2}\nVideo Rate: {3}\nVideo Views: {4}\n"\
    "Video Thumbnail Url: {5}\nVideo Caption: {6}\nVideo Length: {7}".format(vid_title, vid_author, vid_description, 
    vid_rate, vid_views, vid_photo, vid_caption, vid_length)
    print(all_details)

if __name__ == "__main__":
    main_menu()
