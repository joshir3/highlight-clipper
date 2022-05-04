from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from collections import defaultdict   
import pytube
from pytube.exceptions import RegexMatchError
from pytube import YouTube
import re  
from pathlib import Path
# monkey patch cipher.py

def get_throttling_function_name(js: str) -> str:
    """Extract the name of the function that computes the throttling parameter.
    :param str js:
        The contents of the base.js asset file.
    :rtype: str
    :returns:
        The name of the function used to compute the throttling parameter.
    """
    function_patterns = [
        # https://github.com/ytdl-org/youtube-dl/issues/29326#issuecomment-865985377
        # https://github.com/yt-dlp/yt-dlp/commit/48416bc4a8f1d5ff07d5977659cb8ece7640dcd8
        # var Bpa = [iha];
        # ...
        # a.C && (b = a.get("n")) && (b = Bpa[0](b), a.set("n", b),
        # Bpa.length || iha("")) }};
        # In the above case, `iha` is the relevant function name

        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*',
r'\([a-z]\s*=\s*([a-zA-Z0-9$]{2,3})(\[\d+\])?\([a-z]\)'

    ]
    print("fuck")
    print(js)
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            if len(function_match.groups()) == 1:
                return function_match.group(1)
            idx = function_match.group(1)
            if idx:
                idx = idx.strip("[]")
                array = re.search(
                    r'var {nfunc}\s*=\s*(\[.+?\]);'.format(
                        nfunc=function_match.group(1)),
                    js
                )
                if array:
                    array = array.group(1).strip("[]").split(",")
                    array = [x.strip() for x in array]
                    return array[int(idx)]

    raise RegexMatchError(
        caller="get_throttling_function_name", pattern="multiple"
    )


pytube.cipher.get_throttling_function_name = get_throttling_function_name


def timestep(input_file, start_time, end_time, output_name):
    ffmpeg_extract_subclip(input_file, start_time, end_time, output_name)


def read_txt(file_name):
    with open(file_name) as file_handle:
        # do things with the file handle in here
        lines = file_handle.readlines()
        return lines


def make_clips(lines, clips_folder):
    clip_label = defaultdict(int)
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
            strt_min, strt_sec = [int(x) for x in line[1].split(":")]
            strt_time = strt_min*60 + strt_sec
            stp_min, stp_sec = [int(x) for x in line[2].split(":")]
            stp_time = stp_min*60 + stp_sec
            filename = Path(name + str(clip_label[name]) + video_name)
            file_save_path = clips_folder / filename
            timestep(video_name, strt_time, stp_time, str(filename))



def main():
    #vid_path = "Riya sings song.AVI"
    #vid_clip = "clip.avi"
    #clip = VideoFileClip(vid_path).cutout(0, 7)
    #clip.write_videofile(vid_clip, codec='mpeg4')
    #ffmpeg_extract_subclip(vid_path, 0, 5, targetname=vid_clip)
    # by default save the clips to the folder containing the repo
    save_directory = Path(__file__).parent.parent
    # by default use the clips txt file sitting next to main.py
    txt_file = 'links_file.txt'
    a = read_txt(txt_file)
    make_clips(a, save_directory)

if __name__ == "__main__":
    main()
