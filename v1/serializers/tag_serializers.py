from rest_framework import serializers

class TagSerializer(serializers.Serializer):
    tag = serializers.CharField(max_length=255)

