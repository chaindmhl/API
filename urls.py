from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tracking.views import (
    VideoUploadViewSet,
    ProcessVideoViewSet,
    ImageUploadViewSet,
    FrameExtractViewSet,
    
)

router = DefaultRouter()
router.register("tracking/video", VideoUploadViewSet, basename="tracking-video")
router.register("tracking/extract", FrameExtractViewSet, basename="tracking-extract")
router.register("tracking/image", ImageUploadViewSet, basename="tracking-image")
router.register("tracking/tric", ProcessVideoViewSet, basename="tracking-tric")
# TODO: create url for Eye Detection
urlpatterns = [
    path('', include(router.urls)),
]