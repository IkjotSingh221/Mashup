from pytube import YouTube
from youtubesearchpython import VideosSearch
import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import zipfile
from dotenv import load_dotenv
load_dotenv()

email_address = os.getenv("EMAIL_ADDRESS") 
email_password = os.getenv('EMAIL_PASSWORD')     

def mashup_generator(Singer, num, seconds,output_filename):
    Singer = Singer.replace(" ", "+") + "+songs"
    videosSearch = VideosSearch(Singer, limit = num)
    result = videosSearch.result()['result']
    links = []
    for i in range(num):
        links.append(result[i]['link'])
    mp3_files = []
    current_directory = os.getcwd().replace("\\", "/")
    for i,link in enumerate(links, start=1):
        yt = YouTube(link)
        audio = yt.streams.filter(only_audio=True).first()
        file_name = "song{}.mp3".format(i)
        file_path = current_directory + "/" + file_name
        audio.download(filename=file_name)
        mp3_files.append(file_path)
        print("Downloaded: ", yt.title)
    cut_paths=[]
    for song in mp3_files:
        input_name = f"\"{song}\""
        file_name = song.replace(".mp3","")
        output_name = f"\"{file_name}_cut" + ".mp3\""
        command1 = f"ffmpeg -i {input_name} -t {seconds} {output_name}"
        # print(command)
        try:
            os.system(command1)
            os.remove(song)
            cut_paths.append(output_name)
            print(f"{song} cut successfully.")
        except Exception as e:
            print(f"Error occurred while cutting {song}: {e}")
    input_files = "|".join(cut_paths).replace("\"|\"", "|")
    cwd = os.getcwd().replace("\\", "/")
    output_name = cwd + "/" + output_filename
    output_name = f"\"{output_name}\""
    command = f"ffmpeg -i concat:{input_files} -c copy {output_name}"
    print(command)
    try:
        os.system(command)
        print("Audio files merged successfully.")
        for file in cut_paths:
            os.remove(file.replace("\"", ""))
    except Exception as e:
        print(f"Error occurred while merging audio files: {e}")
    

if __name__=="__main__":
    n= len(sys.argv)
    if (n<5):
        print(n)
        print("Number of Arguments did not match!")
        sys.exit(1)
    Singer = sys.argv[1]
    num = int(sys.argv[2])
    if (num<10):
        print("Number of songs should be greater than 10")
        sys.exit(1)
    seconds = int(sys.argv[3])
    if (seconds<20):
        print("Duration should be greater than 20 seconds")
        sys.exit(1)
    output_mp3 = sys.argv[4]
    output_zip = output_mp3.replace(".mp3", ".zip")
    # mashup_generator(Singer, num, seconds, output_mp3)