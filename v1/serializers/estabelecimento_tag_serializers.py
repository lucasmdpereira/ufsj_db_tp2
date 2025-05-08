from rest_framework import serializers

class EstabelecimentoTagSerializer(serializers.Serializer):
    link_google = serializers.CharField(max_length=255)
    tag = serializers.CharField(max_length=255)