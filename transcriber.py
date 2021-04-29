import subprocess
import sys,os
import struct
from pathlib import Path
import requests
from pyunpack import Archive

def get_platform():
    info = []
    platforms = {
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform
    
    return platforms[sys.platform]

operating_system=[get_platform(),str(struct.calcsize("P")*8)]
ffm = str(subprocess.call('ffmpeg -version',shell=True))
curr = Path()
if not (ffm.find('ffmpeg version 3.')):
    if operating_system[0]=='linux' or 'Linux':
        subprocess.call('sudo apt-get install ffmpeg', shell=True)
    elif operating_system[0]=='OS X':
        subprocess.call('brew install ffmpeg', shell=True)
    else:
        url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z'
        r = requests.get(url, allow_redirects=True)
        Archive('../ffmpeg-2021-04-28-git-1ab74bc193-full_build.7z').extractall(curr)
        subprocess.call('Move-Item -Path {curr}\\FFmpeg -Destination C:\\')
        subprocess.call('setx /m PATH "C:\FFmpeg\\bin;%PATH%" -Verb "runAs"')
os.system('python3.7 -m pip install ibm_watson')
# print(operating_system)

from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

filetype = int(input("press 1 for video input\npress 2 for audio input:\n"))
audio_file = ''
    
if filetype == 1:
    video_file = str(input('paste the absolute path of your video file in .mkv or .mp4 format:\n'))
    command = 'ffmpeg -i {video_file} -ab 160k -ar 44100 -vn audio1.mp3'
    subprocess.call(command, shell=True)
    audio_file = 'audio1.mp3'
elif filetype == 2:
    audio_file = str(input('paste the absolute path of your video file in .mp3 format:\n'))


apikey = 'oOaPhBTgxiUKa7qHXpgJ2Tex8actK31pMTDrtRGWYtQk'
url = 'https://api.jp-tok.speech-to-text.watson.cloud.ibm.com/instances/8f3fa8d4-5960-40e1-a0eb-711eb97e3a09'

authenticator = IAMAuthenticator(apikey)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(url)



with open(audio_file, 'rb') as f:
    res = stt.recognize(audio=f, content_type='audio/mp3', model='en-US_BroadbandModel', continuous=True).get_result()

print(res)

len(res['results'])
text = [result['alternatives'][0]['transcript'].rstrip() + '.\n' for result in res['results']]
text = [para[0].title() + para[1:] for para in text]
transcript = ''.join(text)
with open('output.txt', 'w') as out:
    out.writelines(transcript)