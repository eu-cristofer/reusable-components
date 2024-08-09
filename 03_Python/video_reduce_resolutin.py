import os
import ffmpeg

"""
This script scans a specified folder for video files, checks their resolution, 
and converts any FullHD (1920x1080) videos to HD (1280x720). The converted 
videos are saved in a new subfolder named 'HD' within the original folder.

The script performs the following steps:

1. **Scan the Folder**: 
   - The script traverses the given folder and all its subfolders, looking for 
     video files with specific extensions (e.g., .mp4, .mkv, .avi, .mov, .flv).
   
2. **Check Resolution**: 
   - For each video file, the script retrieves its resolution (width and height).
   
3. **Convert FullHD Videos to HD**:
   - If a video file is in FullHD (1920x1080), it is converted to HD (1280x720) 
     using `ffmpeg`. The converted file is saved in the newly created 'HD' folder 
     within the original directory.
   
4. **Handle Errors**:
   - The script handles potential errors, such as issues with probing the video 
     files or problems during the conversion process, by printing error messages.

Modules and Functions:
-----------------------

1. **get_video_resolution(video_path)**:
   - Extracts the resolution (width and height) of the video file.
   
2. **convert_to_hd(video_path, output_path)**:
   - Converts a FullHD video to HD resolution and saves it to the specified path.
   
3. **process_videos_in_folder(folder_path)**:
   - Scans the folder for video files, checks their resolution, and converts 
     FullHD videos to HD, saving them in a new 'HD' folder.

Usage:
------
1. Replace `'/path/to/your/folder'` in the `if __name__ == "__main__"` section 
   with the path of the folder you want to scan.
   
2. Run the script. The script will process all the video files in the specified 
   folder, converting any FullHD videos to HD and saving them in a new `HD` 
   subfolder.

Dependencies:
-------------
- `ffmpeg-python` library: You can install it using `pip install ffmpeg-python`.
- `ffmpeg` command-line tool: Ensure it is installed on your system.

Note:
-----
- The original video files are not modified; only the converted HD videos are 
  saved in the new folder.
- The script skips any video files that are not in FullHD resolution.
"""

def get_video_resolution(video_path):
    """
    Get the resolution of a video file.

    Parameters
    ----------
    video_path : str
        Path to the video file.

    Returns
    -------
    tuple of int or None
        A tuple containing the width and height of the video. 
        Returns None if the resolution cannot be determined.
    """
    try:
        probe = ffmpeg.probe(video_path)
        video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
        if video_streams:
            width = int(video_streams[0]['width'])
            height = int(video_streams[0]['height'])
            return width, height
    except ffmpeg.Error as e:
        print(f"Error probing video {video_path}: {e}")
    return None

def convert_to_hd(video_path, output_path):
    """
    Convert a video to 1280x720 resolution (HD).

    Parameters
    ----------
    video_path : str
        Path to the original video file.
    output_path : str
        Path to save the converted video file.
    """
    try:
        (
            ffmpeg
            .input(video_path)
            .output(output_path, vf='scale=1280:720')
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        print(f"Error converting video {video_path} to HD: {e}")

def process_videos_in_folder(folder_path):
    """
    Scan a folder for video files, check their resolution, and convert FullHD videos to HD.

    Parameters
    ----------
    folder_path : str
        Path to the folder containing video files.
    """
    hd_folder = os.path.join(folder_path, 'HD')
    os.makedirs(hd_folder, exist_ok=True)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv')):
                video_path = os.path.join(root, file)
                resolution = get_video_resolution(video_path)
                if resolution:
                    width, height = resolution
                    if width == 1920 and height == 1080:  # FullHD resolution
                        print(f"Converting {video_path} to HD...")
                        output_path = os.path.join(hd_folder, file)
                        convert_to_hd(video_path, output_path)
                        print(f"Converted {file} to HD (720p) and saved to {output_path}.")
                    else:
                        print(f"{file} is not FullHD (1920x1080), skipping conversion.")
                else:
                    print(f"Could not determine resolution for {file}, skipping.")

if __name__ == "__main__":
    # Set the folder path to scan
    folder_path = '/path/to/your/folder'
    process_videos_in_folder(folder_path)
