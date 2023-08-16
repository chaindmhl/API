from django.contrib import admin
from .models import Video, PlateLog

# Register your models here.
admin.site.register(Video)
#admin.site.register(PlateLog)

class PlateLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'display_frame_image', 'display_plate_image', 'plate_number' )  # Include 'display_plate_image' here

admin.site.register(PlateLog, PlateLogAdmin)
