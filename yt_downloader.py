import PySimpleGUI as sg # Imports PySimpleGUI, for a GUI.
from pytube import YouTube # Imports PyTube, for downloading YouTube videos.
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips  # imports moviepy's required functions, for merging audio and video.
import requests, os, threading # imports requests, for checking that a YouTube url is valid. imports os for checking if files exist. Imports threading
from datetime import timedelta # imports timedelta, for converting seconds into the hh:mm:ss format.

tempPath = '.\\temp\\'
sg.theme('DefaultNoMoreNagging')

def check_validity(link):
    if link != 'youtube.com' and link != 'youtu.be':
        if 'youtube.com' in link or 'youtu.be' in link:  
            request = requests.get(link)
            if not 'Video unavailable' in request.text:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def refresh_info(window):
    length = str(timedelta(seconds = yt.length))
    views = ('{:,}'.format(yt.views))
    
    window['-YT TITLE-'].update(yt.title)
    window['-YT CHANNEL-'].update(yt.author)
    window['-YT LENGTH-'].update(length)
    window['-YT VIEWS-'].update(views)
   
def stream_select(window):
    # ---------- configuring seperate sections ----------
    layout1 = [[sg.Text('Select a Resolution:', font='Default 10 bold')], [sg.HSeparator()]]
    layout2 = []
    layout3 = [[sg.Button('Select'), sg.Button('Cancel')]]
    
    # ---------- main layout ----------
    
    count = 0
    resolutions = []
    res_to_itag = {}
    
    for i in yt.streams.filter(only_video=True):

        if '2160p' in str(i) and not '4k' in resolutions:
            resolutions.append('4k')
            stream = yt.streams.filter(only_video=True, resolution='2160p').order_by('resolution').desc().first()
            itag = stream.itag
            res_to_itag['4k'] = itag
        elif '1440p' in str(i) and not '1440p' in resolutions:
            resolutions.append('1440p')
            stream = yt.streams.filter(only_video=True, resolution='1440p').order_by('resolution').desc().first()
            itag = stream.itag
            res_to_itag['1440p'] = itag
        elif '1080p' in str(i) and not '1080p' in resolutions:
            resolutions.append('1080p')
            stream = yt.streams.filter(only_video=True, resolution='1080p').order_by('resolution').desc().first()
            itag = stream.itag
            res_to_itag['1080p'] = itag
        elif '720p' in str(i) and not '720p' in resolutions:
            resolutions.append('720p')
            stream = yt.streams.filter(only_video=True, resolution='720p').order_by('resolution').desc().first()
            itag = stream.itag
            res_to_itag['720p'] = itag
        elif '480p' in str(i) and not '480p' in resolutions:
            resolutions.append('480p')
            stream = yt.streams.filter(only_video=True, resolution='480p').order_by('resolution').desc().first()
            itag = stream.itag
            res_to_itag['480p'] = itag
        elif '360p' in str(i) and not '360p' in resolutions:
            resolutions.append('360p')
            stream = yt.streams.filter(only_video=True, resolution='360p').order_by('resolution').desc().first()
            itag = stream.itag
            res_to_itag['360p'] = itag
        elif '240p' in str(i) and not '240p' in resolutions:
            resolutions.append('240p')
            stream = yt.streams.filter(only_video=True, resolution='240p').order_by('resolution').desc().first()
            itag = stream.itag
            res_to_itag['240p'] = itag
        elif '144p' in str(i) and not '144p' in resolutions:
            resolutions.append('144p')
            stream = yt.streams.filter(only_video=True, resolution='144p').order_by('resolution').desc().first()
            itag = stream.itag
            res_to_itag['144p'] = itag
        
    for i in resolutions:
        if count == 0:
            layout2.append([sg.Radio(i, 'Radio', default=True, key='-%s-' % i)])
            count += 1
        else:
            layout2.append([sg.Radio(i, 'Radio', key='-%s-' % i)])
            count += 1
            
    layout = [[sg.Column(layout1)], [sg.Column(layout2)], [sg.Column(layout3)]]
        
    stream_window = sg.Window('Stream Select', layout, icon='yt_dl.ico')
    
    while True:
        event, values = stream_window.read()
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        elif event == 'Select':
            if values['-144p-']:
                stream_window.close()
                dl = threading.Thread(target=download, args=(res_to_itag['144p'], window))
                dl.start()
            elif values['-240p-']:
                stream_window.close()
                dl = threading.Thread(target=download, args=(res_to_itag['240p'], window))
                dl.start()
            elif values['-360p-']:
                stream_window.close()
                dl = threading.Thread(target=download, args=(res_to_itag['360p'], window))
                dl.start()
            elif values['-480p-']:
                stream_window.close()
                dl = threading.Thread(target=download, args=(res_to_itag['480p'], window))
                dl.start()
            elif values['-720p-']:
                stream_window.close()
                dl = threading.Thread(target=download, args=(res_to_itag['720p'], window))
                dl.start()
            elif values['-1080p-']:
                stream_window.close()
                dl = threading.Thread(target=download, args=(res_to_itag['1080p'], window))
                dl.start()
            elif values['-1440p-']:
                stream_window.close()
                dl = threading.Thread(target=download, args=(res_to_itag['1440p'], window))
                dl.start()
            elif values['-4k-']:
                stream_window.close()
                dl = threading.Thread(target=download, args=(res_to_itag['4k'], window))
                dl.start()
        
    stream_window.close()
    
def download(itag, window):
    
    title = yt.title
    pathPrompt = sg.popup_get_file('Download Path',save_as=True, no_window=True, default_path=title, default_extension='.mp4', file_types=(('MPEG-4','*.mp4'),), icon='yt_dl.ico')
    if len(pathPrompt) > 0:
        downloadPath = pathPrompt
    
        window['-DOWNLOADING-'].update(visible=True)
        window['-DL COMPLETE-'].update(visible=False)
        window['Download'].update(disabled=True)
        window['Search'].update(disabled=True)
        
        videoStream = yt.streams.get_by_itag(itag)
        audioStream = yt.streams.filter(adaptive=True,only_audio=True).order_by('abr').desc().first()
        
        if 'mp4' in str(videoStream):
            video = 'video.mp4'
        elif 'webm' in str(videoStream):
            video = 'video.webm'
        
        if 'mp4' in str(audioStream):
            audio = 'audio.mp4'
        elif 'webm' in str(audioStream):
            audio = 'audio.webm'
        
        videoStream.download(output_path=tempPath, filename=video)
        audioStream.download(output_path=tempPath, filename=audio)
        
        video = VideoFileClip(str(tempPath)+str(video))
        audio = AudioFileClip(str(tempPath)+str(audio))
        merge = concatenate_videoclips([video.set_audio(audio)])
        merge.write_videofile(downloadPath)
        
        clear_temp()
        
        pathPrompt = ''
        
        window['-DOWNLOADING-'].update(visible=False)
        window['-DL COMPLETE-'].update(visible=True)
        window['Download'].update(disabled=False)
        window['Search'].update(disabled=False)

def clear_temp():
    for f in os.listdir(tempPath):
        os.remove(os.path.join(tempPath, f))

def main():
    # everything to do with the GUI, and structuring the program
    # ---------- configuring seperate layouts ----------
    layout1 = [
        [sg.Text('Enter YouTube video link:')],
        [sg.Input(key='-LINK-')],
        [sg.Button('Search'), sg.Text('Invalid YouTube Link', text_color='#ff0000', key='-SEARCH ERROR1-', visible=False)]  
    ]
    
    layout2 = [
        [sg.HSeparator()],
        [sg.Text('Title:', font='Default 10 bold'), sg.Text('', key='-YT TITLE-')],
        [sg.Text('Channel:', font='Default 10 bold'), sg.Text('', key='-YT CHANNEL-')],
        [sg.Text('Length:', font='Default 10 bold'), sg.Text('', key='-YT LENGTH-')],
        [sg.Text('Views:', font='Default 10 bold'), sg.Text('', key='-YT VIEWS-')],
        [sg.Button('Download'),sg.Text('Downloading...  (This may take some time.)', key='-DOWNLOADING-', visible=False), sg.Text('Downloaded', text_color='#009e1f', key='-DL COMPLETE-', visible=False)]
    ]
    
    # ---------- main layout ----------
    
    layout = [
        [sg.Column(layout1)],
        [sg.Column(layout2, key='-LAYOUT2-', visible=False)]
        
    ]
    
    window = sg.Window('YT Downloader', layout, icon='yt_dl.ico')
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Search':
            window['-DL COMPLETE-'].update(visible=False)
            window['-DOWNLOADING-'].update(visible=False)
            if check_validity(values['-LINK-']) == True:
                window['-SEARCH ERROR1-'].update(visible=False)
                global yt
                yt = YouTube(values['-LINK-'])
                window['-LAYOUT2-'].update(visible=True)
                refresh_info(window) # refreshes info such as video title and length
            else:
                window['-SEARCH ERROR1-'].update(visible=True)
                window['-LAYOUT2-'].update(visible=False)
        elif event == 'Download':
            stream_select(window)
                
    window.close()
    
main()