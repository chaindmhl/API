from rest_framework import serializers
from tracking.models import (
    Video,
    # Frame,
    Image,
)


class VideoSerializers(serializers.ModelSerializer):
    file = serializers.FileField(max_length=500)

    class Meta:
        model = Video
        fields = ["id", "file", "user"]

    def create(self, validated_data):
        return Video.objects.create(**validated_data)


class ImageSerializers(serializers.ModelSerializer):
    file = serializers.FileField(max_length=500)

    class Meta:
        model = Image
        fields = ["id", "file", "user", "video"]

    def create(self, validated_data):
        return Image.objects.create(**validated_data)


class FrameExtractionSerializers(serializers.Serializer):
    video = serializers.PrimaryKeyRelatedField(queryset=Video.objects.all())

    def create(self, validated_data):
        video = validated_data["video"]
        return video
    
class TricycleDetectionSerializers(serializers.Serializer):
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())

    def create(self, validated_data):
        image = validated_data["image"]
        return image
    
class ProcessVideoSerializers(serializers.Serializer):
    video = serializers.PrimaryKeyRelatedField(queryset=Video.objects.all())

    def create(self, validated_data):
        video = validated_data["video"]
        return video