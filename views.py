from rest_framework import viewsets, status
from rest_framework.response import Response
from tracking.serializers import (
    TricycleDetectionSerializers,
    VideoSerializers,
    ImageSerializers,
    FrameExtractionSerializers,
    ProcessVideoSerializers,
)
from tracking.models import Video, Image
from tracking.extract import (
    frame_extract,
)
from tracking.process import process_vid
import tensorflow as tf

# Load your own model
model_path = "/home/itwatcher/tricycle/tracking/tric_files/checkpoints"
model = tf.saved_model.load(model_path)


# Define your Django Rest Framework view
from rest_framework.response import Response


# Create your views here.
class VideoUploadViewSet(viewsets.ModelViewSet):
    """
    Uploads a File
    """

    queryset = Video.objects.all()
    serializer_class = VideoSerializers


class ImageUploadViewSet(viewsets.ModelViewSet):
    """
    Uploads a File
    """

    queryset = Image.objects.all()
    serializer_class = ImageSerializers


class FrameExtractViewSet(viewsets.ViewSet):
    """
    Frame Extraction
    """

    serializer_class = FrameExtractionSerializers

    def create(self, request):
        serializer = FrameExtractionSerializers(data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            images = frame_extract(video)
            context = {"video": video.id, "images": images}
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TricycleDetectViewSet(viewsets.ViewSet):
    """
    Face Detection
    """

    serializer_class = TricycleDetectionSerializers

    def create(self, request):
        serializer = TricycleDetectionSerializers(data=request.data)
        if serializer.is_valid():
            image = serializer.save()
            frame_id = tric_detect(image)
            context = {"image": image.id, "frame": frame_id}
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# TODO: Create Viewset for Eye Detection
# class EyeDetectViewSet(viewsets.ViewSet):


class ProcessVideoViewSet(viewsets.ViewSet):
    """
    Perform tricycle Detection in Videos
    """

    serializer_class = ProcessVideoSerializers

    def create(self, request):
        serializer = ProcessVideoSerializers(data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            context = process_vid(video)
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
