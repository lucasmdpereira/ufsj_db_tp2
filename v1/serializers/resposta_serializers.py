from rest_framework import serializers

class RespostaSerializer(serializers.Serializer):
    data_review_id = serializers.CharField(max_length=255)
    texto = serializers.CharField(max_length=1000)
    data = serializers.DateField()
