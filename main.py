from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from collections import defaultdict   
from pytube import YouTube 
import re  


def timestep(input_file, start_time, end_time, output_name):
    ffmpeg_extract_subclip(input_file, start_time, end_time, output_name)


def read_txt(file_name):
    with open(file_name) as file_handle:
        # do things with the file handle in here
        lines = file_handle.readlines()
        print(lines)
        return lines


def make_clips(lines):
    clip_label = defaultdict(int)
    SAVE_PATH = r"C:\\Users\\TJ-LPTP\Desktop\\Volleyball"
    d_video=None
    for line in lines:
        if line.strip() == "":
            continue

        elif line.startswith("https://"):
            yt = YouTube(line)
            video_name = yt.title.replace('.','') + '.mp4'
            stream = yt.streams.filter(progressive=True).last()
            stream.download()

        else:
            line = line.strip()
            line = line.split(',')
            name = line[0]
            clip_label[name] += 1
            print("I'M TRAPPED INSIDE THE COMPUTER HELP THIS IS NOT A JOKE")
            print(line)
            strt_min, strt_sec = [int(x) for x in line[1].split(":")]
            strt_time = strt_min*60 + strt_sec
            stp_min, stp_sec = [int(x) for x in line[2].split(":")]
            stp_time = stp_min*60 + stp_sec
            filename = name + str(clip_label[name]) + video_name
            timestep(video_name, strt_time, stp_time, filename)



def main():
    #vid_path = "Riya sings song.AVI"
    #vid_clip = "clip.avi"
    #clip = VideoFileClip(vid_path).cutout(0, 7)
    #clip.write_videofile(vid_clip, codec='mpeg4')
    #ffmpeg_extract_subclip(vid_path, 0, 5, targetname=vid_clip)
    txt_file = 'links_file.txt'
    a = read_txt(txt_file)
    make_clips(a)
    
    

if __name__ == "__main__":
    main()
