#!/usr/bin/python3
import os, sys, datetime, subprocess, shutil

if len(sys.argv) < 3:
    print("Usage: python3 neo-media-importer.py <WORKING-DIRECTORY> <TARGET-DIRECTORY>")
    print("If more arguments are passed, every video will be encoded to h264.")
    exit(1)

working_directory = os.path.dirname(os.path.abspath(sys.argv[1]))
target_directory = os.path.abspath(sys.argv[2])

for path, dirs, files in os.walk(working_directory):
    for file in files:
        if file.startswith("DJI_") and file.endswith(".MP4"):
            file_id = file.removesuffix(".MP4") # filename without .MP4 (such as DJI_20250101151617_0023_D)
            full_video_path = os.path.join(path, file)
            full_flightdata_path = os.path.join(path, file_id + ".SRT")
            full_audio_path = os.path.join(path, file_id + ".m4a")

            time = os.path.getmtime(full_video_path)
            date_str = datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%d-%H:%M:%S")

            new_video_path = os.path.join(target_directory, date_str + ".mp4")
            new_flightdata_path = os.path.join(target_directory, date_str + ".srt")

            print("Processing %s" % (file_id))
            print()

            if len(sys.argv) > 3:
                if os.path.exists(full_audio_path):
                    subprocess.run(["ffmpeg", "-i", full_video_path, "-i", full_audio_path, "-c:v", "h264", "-c:a", "aac", new_video_path]) # ffmpeg -i DJI_20250101151617_0023_D.MP4 -i DJI_20250101151617_0023_D.m4a -c:v h264 -c:a aac 2025-01-01-15:16:17.mp4
                else:
                    subprocess.run(["ffmpeg", "-i", full_video_path, "-c:v", "h264", new_video_path]) # ffmpeg -i DJI_20250101151617_0023_D.MP4 -c:v h264 2025-01-01-15:16:17.mp4
            else:
                if os.path.exists(full_audio_path):
                    subprocess.run(["ffmpeg", "-i", full_video_path, "-i", full_audio_path, "-c:v", "copy", "-c:a", "aac", new_video_path]) # ffmpeg -i DJI_20250101151617_0023_D.MP4 -i DJI_20250101151617_0023_D.m4a -c:v copy -c:a aac 2025-01-01-15:16:17.mp4
                else:
                    shutil.copy2(full_video_path, new_video_path)

            shutil.copy2(full_flightdata_path, new_flightdata_path)
        elif file.startswith("DJI_") and file.endswith(".JPG"):
            file_id = file.removesuffix(".JPG")
            full_photo_path = os.path.join(path, file)

            time = os.path.getmtime(full_photo_path)
            date_str = datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%d-%H:%M:%S")

            new_photo_path = os.path.join(target_directory, date_str + ".jpg")

            print("Processing %s" % (file_id))
            print()
            shutil.copy2(full_photo_path, new_photo_path)
