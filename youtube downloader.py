# !usr/bin/dev python
from pytube import YouTube
import os, time, sys
from win10toast import ToastNotifier
from pynotifier import Notification 

# color table
ENDC = '\033[0m'
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
CYAN = '\033[96m'
YELLOW = '\033[93m'

def main_menu():
    while True:
        global url_input
        url_input = input("enter video url : ")
        try:
            global youtube_connect
            youtube_connect = YouTube(url_input)
            print("\n\nTitle : {0}\nAuthor : {1}\nCaptions : {2}\nDescription : {3}\nVideo Length : {4}\nRate : {5}\nViews : {6}"
            "\nphoto : {7}".format(title(), author(), caption(), description(), length(), rate(), views(), photo()))
            menu_input = int(input("\n1.Download\n2.enter new url\n3.Exit\n: "))
            if menu_input == 1:
                download()
            elif menu_input == 2:
                main_menu()
            elif menu_input == 3:
                print("bye")
                exit()
            else:
                print(f"{RED}invalid entry !!{ENDC}")
                main_menu()
        except TypeError:
            print(f"{RED}invalid entry !!{ENDC}")
            break
def notify():
    # windows
    plat = sys.platform()
    if plat == 'win32':
        toaster = ToastNotifier()
        toaster.show_toast("Download Finished", "youtube downloader download finished", duration=6,)
    # linux
    elif plat == 'linux':
        Notification(title="Download Finished", description="youtube downloader download finished", duration=6, urgency=Notification.URGENCY_NORMAL).send()

def download():
    while True:
        dl_path = os.path.expanduser('~/Downloads/')
        ytd_dl_path = os.path.expanduser('~/Downloads/YTD')
        os.chdir(dl_path)  
        try:          
            os.mkdir('YTD')
        except FileExistsError:
            pass
        # try:
        video_quality = int(input("\n1.360p\n2.480p\n3.720p\n4.main menu\n: "))
        # 360 p -----
        if video_quality == 1:
            stream_360 = youtube_connect.streams.filter(res='360p').first()
            path = input("enter exact path for file to save, or leave empty to defualt(~/Download/YTD/): ")
            if path == '' or None:
                os.chdir(ytd_dl_path)

                try:
                    print("press Ctrl+c to cancel download any time")
                    stream_360.download(ytd_dl_path)
                    notify()
                except KeyboardInterrupt:
                    print(f"{RED}download canceled !!{ENDC}")

            else:
                os.chdir(path)

                try:
                    print("press Ctrl+c to cancel download any time")
                    stream_360.download(path)
                    notify()
                except KeyboardInterrupt:
                    print(f"{RED}download canceled !!{ENDC}")
        # 480 p -----
        elif video_quality == 2:
            stream_480 = youtube_connect.streams.filter(res='480p').first()
            path = input("enter exact path for file to save, or leave empty to defualt(~/Download/YTD/): ")
            if path == '' or None:
                os.chdir(ytd_dl_path)

                try:
                    print("press Ctrl+c to cancel download any time")
                    stream_480.download(ytd_dl_path)
                    notify()
                except KeyboardInterrupt:
                    print(f"{RED}download canceled !!{ENDC}")
            else:
                os.chdir(path)
                try:
                    print("press Ctrl+c to cancel download any time")
                    stream_480.download(path)
                    notify()
                except KeyboardInterrupt:
                    print(f"{RED}download canceled !!{ENDC}")
        # 720 p -----
        elif video_quality == 3:
            stream_720 = youtube_connect.streams.filter(res='720p').first()
            path = input("enter exact path for file to save, or leave empty to defualt(~/Download/YTD/): ")
            if path == '' or None:
                os.chdir(ytd_dl_path)
                try:
                    print("press Ctrl+c to cancel download any time")
                    stream_720.download(ytd_dl_path)
                    notify()
                except KeyboardInterrupt:
                    print(f"{RED}download canceled !!{ENDC}")
            else:
                os.chdir(path)
                try:
                    print("press Ctrl+c to cancel download any time")
                    stream_720.download(path)
                    notify()
                except KeyboardInterrupt:
                    print(f"{RED}download canceled !!{ENDC}")
        elif video_quality == 4:
            main_menu()
        else:
            print(f"{RED}invalid entry{ENDC} ")
            download()
        # except Exception:
        #     print(f"{YELLOW}something goes wrong check your internet and try again later !!!{ENDC}")
        


def title():
    vid_title = youtube_connect.title
    return vid_title

def author():
    vid_author = youtube_connect.author
    return vid_author

def caption():
    vid_caption = youtube_connect.captions
    if vid_caption == '' or vid_caption is None or vid_caption == {}:
        vid_caption = "video has no caption"
    return vid_caption

def description():
    vid_description = youtube_connect.description
    return vid_description

def length():
    vid_length = youtube_connect.length
    if vid_length >= 60:
        vid_length //= 60
        return str(vid_length) + "'M"
    elif vid_length < 60:
        return str(vid_length) + "'S"

def rate():
    vid_rate = youtube_connect.rating
    return vid_rate

def views():
    vid_views = youtube_connect.views
    return vid_views

def photo():
    vid_photo = youtube_connect.thumbnail_url
    return vid_photo

if __name__ == "__main__":
    main_menu()
