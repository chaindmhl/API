from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tracking.views import (
    VideoUploadViewSet,
    ProcessVideoViewSet,
    CatchAllViewSet,
    LPRViewSet,
    MyView,
    PlateView,
    FrameView,
    MapView,
    
)

router = DefaultRouter()
router.register("tracking/video", VideoUploadViewSet, basename="tracking-video")
router.register("tracking/tric", ProcessVideoViewSet, basename="tracking-tric")
router.register("tracking/lpr", LPRViewSet, basename="LPR-tric")
router.register("tracking/catchall", CatchAllViewSet, basename="tracking-catchall")

urlpatterns = [
    path('', include(router.urls)),
    path('my-url/', MyView.as_view(), name='my-view'),
    path('display_plates/', PlateView.as_view(), name='display_plates'),
    path('view_frame/<int:log_id>/', FrameView.view_frame, name='view_frame'),
    path('view_camera_map/<int:log_id>/', MapView.view_camera_map, name='view_camera_map'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
