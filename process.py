import requests
from django.conf import settings
from json.decoder import JSONDecodeError
from tracking.extract import (
    frame_extract,
)
from tracking.models import Image
import os
import cv2
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
from tracking.deepsort_tric.object_tracker import VehiclesCounting
from tracking.models import Video, Frame
from .serializers import VideoSerializers

import numpy as np
import tensorflow as tf

REQUEST_URL = f"http://{settings.HOST}:8000/"


'''def process_vid(video):
    # Frame Extraction
    try:
        response = requests.post(
            REQUEST_URL + "tracking/extract/",
            json={"video": video.id},
        ).json()
        image_ids = response["images"]
    except JSONDecodeError:
        image_ids = frame_extract(video)

    # Tricycle Detection
    frame_ids = tric_detect(video)

    # TODO: Eye Detection
    target_ids = []

    return {
        "video": video.id,
        "images": image_ids,
        "frames": frame_ids,
        "targets": target_ids,
    }'''
def process_vid(video):
   
    # Tricycle Detection and Tracking
    # Load the video file
    video_file = os.path.join(settings.MEDIA_ROOT, str(video.file))
   

        # Create a folder to store the output frames
    output_folder_path = os.path.join(settings.MEDIA_ROOT, 'tracked_videos', str(video.id))
    os.makedirs(output_folder_path, exist_ok=True)

    # Specify the filename and format of the output video
    output_video_path = os.path.join(output_folder_path, f"tracked_{video.id}.mp4")
    

    # Create an instance of the VehiclesCounting class
    vc = VehiclesCounting(file_counter_log_name='vehicle_count.log',
                          framework='tf',
                          weights='/home/itwatcher/tricycle/tracking/deepsort_tric/checkpoints/yolov4-416',
                          size=416,
                          tiny=False,
                          model='yolov4',
                          video= video_file,
                          output=output_video_path,
                          output_format='XVID',
                          iou=0.45,
                          score=0.5,
                          dont_show=False,
                          info=False,
                          detection_line=(0.5, 0))

    vc.run()

    # Perform object tracking on the video frames
    '''tracked_frames = vc.run(cap)

    # Save the frames with object tracking performed on them
    frame_ids = []
    for i, frame in enumerate(tracked_frames):
        # Draw bounding boxes around the tracked objects
        for obj in frame:
            bbox = obj['bbox']
            cv2.rectangle(frame, bbox[0:2], bbox[2:4], (0, 255, 0), 2)

        # Save the frame as an image after object tracking has been performed on it
        _, buffer = cv2.imencode(".jpg", frame)
        content = ContentFile(BytesIO(buffer).getvalue())
        frame_data = {"user": video.user, "video": video}
        frame_instance = Frame.objects.create(**frame_data, file=content)
        frame_instance.file.save(
            f"tric{video.id}_{i}.jpg", content, save=True
        )
        print(f"Extracted frame id: {frame_instance.id}")
        frame_ids.append(frame_instance.id)

    cap.release()

    return {
        "video": video.id,
        "images": image_ids,
        "frames": frame_ids,
    }'''

