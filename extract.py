import os
import cv2
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
from tracking.models import Image, Frame, Target, Video
from tracking.deepsort_tric import object_tracker
from tracking.deepsort_tric.object_tracker import VehiclesCounting
from tracking.models import Video
from .serializers import VideoSerializers

import numpy as np
import tensorflow as tf


def frame_extract(video_instance):
    images = []
    video_file = os.path.join(settings.MEDIA_ROOT, str(video_instance.file))
    cap = cv2.VideoCapture(video_file)
    frame_no = 1
    while True:
        # reading frame from the video source
        ret, frame = cap.read()
        if ret:
            if frame_no % 50 == 9:
                frame = cv2.resize(frame, (960, 540))
                _, buffer = cv2.imencode(".jpg", frame)
                content = ContentFile(BytesIO(buffer).getvalue())
                image_data = {"user": video_instance.user, "video": video_instance}
                image = Image.objects.create(**image_data)
                image.file.save(
                    f"tric{video_instance.id}_{image.id}.jpg", content, save=True
                )
                images.append(image.id)
                print(f"Extracted image id: {image.id}")
            frame_no += 1
        else:
            break
    cap.release()
    return images

'''def tric_detect(video_instance):
    # Load the video file
    video_file = os.path.join(settings.MEDIA_ROOT, str(video_instance.file))
    cap = cv2.VideoCapture(video_file)

    # Create an instance of the VehiclesCounting class
    vc = VehiclesCounting(file_counter_log_name='vehicle_count.log',
                          framework='tf',
                          weights='/home/itwatcher/tricycle/tracking/deepsort_tric/checkpoints/yolov4-416',
                          size=416,
                          tiny=False,
                          model='yolov4',
                          video=video_file,
                          output=None,
                          output_format='XVID',
                          iou=0.45,
                          score=0.5,
                          dont_show=False,
                          info=False,
                          detection_line=(0.5, 0))

    frame_count = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Perform object detection on the frame
        detected_objects = vc.detect(frame)

        # Draw bounding boxes around the detected objects
        for obj in detected_objects:
            bbox = obj['bbox']
            cv2.rectangle(frame, bbox[0:2], bbox[2:4], (0, 255, 0), 2)

        # Save the frame as an image after object detection has been performed on it
        _, buffer = cv2.imencode(".jpg", frame)
        content = ContentFile(BytesIO(buffer).getvalue())
        frame_data = {"user": video_instance.user, "video": video_instance}
        frame_instance = Frame.objects.create(**frame_data, file=content)
        frame_instance.file.save(
            f"tric{video_instance.id}_{frame_instance.id}.jpg", content, save=True
        )
        print(f"Extracted frame id: {frame_instance.id}")

    cap.release()




    _, buffer = cv2.imencode(".jpg", frame)
        content = ContentFile(BytesIO(buffer).getvalue())
        frame_data = {"user": video_instance.user, "video": video_instance}
        frame_instance = Frame.objects.create(**frame_data, file=content)
        frame_instance.file.save(
            f"tric{video_instance.id}_{frame_instance.id}.jpg", content, save=True
        )
        frame_id = frame_instance.id
        print(f"Extracted frame id: {frame_id}")

    cap.release()
    return frame_id'''

