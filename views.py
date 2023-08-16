from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.views import View
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.response import Response
from tracking.serializers import (
    VideoSerializers,
    ProcessVideoSerializers,
    LPRSerializers,
)
from tracking.models import Video, PlateLog
from tracking.process import process_vid
from tracking.process_lpr import process_vidlpr
from tracking.process_all import process_all


# Define your Django Rest Framework view
from rest_framework.response import Response

# Create your views here.
class MyView(View):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        videos = Video.objects.filter(user=request.user)
        context = {'users': users, 'videos': videos}
        return render(request, 'index.html', context)
    
# Create your views here.
class VideoUploadViewSet(viewsets.ModelViewSet):
    """
    Uploads a File
    """

    queryset = Video.objects.all()
    serializer_class = VideoSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProcessVideoViewSet(viewsets.ViewSet):
    """
    Perform tricycle Detection in Videos
    """

    serializer_class = ProcessVideoSerializers

    def create(self, request):
        serializer = ProcessVideoSerializers(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            video_path = data.get("video")
            livestream_url = data.get("camera_feed_url")

            if video_path:
                context = process_vid(video_path=video_path)
            elif livestream_url:
                stream_path = livestream_url
                #stream_file = cv2.VideoCapture(stream_path)
                context = process_vid(livestream_url=livestream_url, video_stream=stream_path)
            else:
                return Response({"error": "Either video or camera_feed_url must be provided"}, status=status.HTTP_400_BAD_REQUEST)

             # Return the path to the output video
            return Response({'output_video_path': context['output_video_path']}, status=status.HTTP_200_OK)

        # Return validation errors if any
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CatchAllViewSet(viewsets.ViewSet):
    """
    Perform tricycle Detection in Videos
    """

    serializer_class = ProcessVideoSerializers

    def create(self, request):
        serializer = ProcessVideoSerializers(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            video_path = data.get("video")
            livestream_url = data.get("camera_feed_url")

            if video_path:
                context = process_all(video_path=video_path)
            elif livestream_url:
                stream_path = livestream_url
                #stream_file = cv2.VideoCapture(stream_path)
                context = process_all(livestream_url=livestream_url, video_stream=stream_path)
            else:
                return Response({"error": "Either video or camera_feed_url must be provided"}, status=status.HTTP_400_BAD_REQUEST)

             # Return the path to the output video
            return Response({'output_video_path': context['output_video_path']}, status=status.HTTP_200_OK)

        # Return validation errors if any
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LPRViewSet(viewsets.ViewSet):
    """
    Perform tricycle Detection in Videos
    """

    serializer_class = LPRSerializers

    def create(self, request):
        serializer = ProcessVideoSerializers(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            video_path = data.get("video")
            livestream_url = data.get("camera_feed_url")

            if video_path:
                context = process_vidlpr(video_path=video_path)
            elif livestream_url:
                stream_path = livestream_url
                #stream_file = cv2.VideoCapture(stream_path)
                context = process_vidlpr(livestream_url=livestream_url, video_stream=stream_path)
            else:
                return Response({"error": "Either video or camera_feed_url must be provided"}, status=status.HTTP_400_BAD_REQUEST)

             # Return the path to the output video
            return Response({'output_video_path': context['output_video_path']}, status=status.HTTP_200_OK)

        # Return validation errors if any
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PlateView(View):

    def get(self, request):
        plate_logs = PlateLog.objects.all()
        context = {
            'plate_logs': plate_logs,
        }
        return render(request, '/home/itwatcher/API/tricycle_copy/tracking/display_plates.html', context)
    def post(self, request):
        # Handle POST requests if needed
        pass
    
class FrameView(View):

    def view_frame(request, log_id):
        # Retrieve the PlateLog instance based on the log_id
        plate_log = PlateLog.objects.get(id=log_id)
        
        context = {
            'plate_log': plate_log,
        }
        return render(request, '/home/itwatcher/API/tricycle_copy/tracking/view_frame.html', context)
    
class MapView(View):

    def view_camera_map(request, log_id):
        plate_log = PlateLog.objects.get(id=log_id)
        context = {
            'plate_log': plate_log,
        }
        return render(request, '/home/itwatcher/API/tricycle_copy/tracking/view_camera_map.html', context)
