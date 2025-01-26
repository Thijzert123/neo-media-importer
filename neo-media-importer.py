#!/usr/bin/python3
import os, sys, datetime, subprocess, shutil

if len(sys.argv) < 3:
    print("Usage: python3 neo-media-importer.py <SOURCE-DIRECTORY> <TARGET-DIRECTORY> [OPTIONS ...]")
    print("Options:")
    print("  -to-h264      Encode videos to h264")
    print("  -merge-audio  Merge audio and videos into one mp4 file")
    exit(1)

source_directory = os.path.dirname(os.path.abspath(sys.argv[1]))
target_directory = os.path.abspath(sys.argv[2])

for path, dirs, files in os.walk(source_directory):
    for file in files:
        if file.startswith("DJI_") and file.endswith(".MP4"):
            file_id = file.removesuffix(".MP4") # filename without .MP4 (such as DJI_20250101151617_0023_D)
            full_video_path = os.path.join(path, file)
            full_flightdata_path = os.path.join(path, file_id + ".SRT")
            full_audio_path = os.path.join(path, file_id + ".m4a")

            time = file_id.split("_")[1]
            date_str = datetime.datetime.strptime(time, "%Y%m%d%H%M%S").strftime("%Y-%m-%d-%H:%M:%S")

            new_video_path = os.path.join(target_directory, date_str + ".mp4")
            new_flightdata_path = os.path.join(target_directory, date_str + ".srt")

            if os.path.exists(new_video_path):
                print("Skipping %s, %s exists" % (file_id, new_video_path))
                print()
                continue

            print("Processing %s (%s)" % (file_id, new_video_path))
            print()

            if "-merge-audio" in sys.argv and os.path.exists(full_audio_path):
                cv_stream_arg = "copy"
                if "-to-h264" in sys.argv:
                    cv_stream_arg = "h264"
                subprocess.run(["ffmpeg", "-i", full_video_path, "-i", full_audio_path, "-c:v", cv_stream_arg, "-c:a", "aac", new_video_path]) # ffmpeg -i DJI_20250101151617_0023_D.MP4 -i DJI_20250101151617_0023_D.m4a -c:v h264 -c:a aac 2025-01-01-15:16:17.mp4
            elif "-to-h264" in sys.argv:
                subprocess.run(["ffmpeg", "-i", full_video_path, "-c:v", "h264", new_video_path]) # ffmpeg -i DJI_20250101151617_0023_D.MP4 -c:v h264 2025-01-01-15:16:17.mp4
            else:
                shutil.copy2(full_video_path, new_video_path)

            shutil.copy2(full_flightdata_path, new_flightdata_path)
        elif file.startswith("DJI_") and file.endswith(".JPG"):
            file_id = file.removesuffix(".JPG")
            full_photo_path = os.path.join(path, file)

            time = file_id.split("_")[1]
            date_str = datetime.datetime.strptime(time, "%Y%m%d%H%M%S").strftime("%Y-%m-%d-%H:%M:%S")

            new_photo_path = os.path.join(target_directory, date_str + ".jpg")

            if os.path.exists(new_photo_path):
                print("Skipping %s, %s exists" % (file_id, new_photo_path))
                print()
                continue

            print("Processing %s (%s)" % (file_id, new_photo_path))
            print()
            shutil.copy2(full_photo_path, new_photo_path)
