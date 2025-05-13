from rest_framework import serializers


class ResumoDeAvaliacoesSerializer(serializers.Serializer):
    link_google = serializers.CharField(max_length=255)
    qtd_avaliacoes = serializers.IntegerField()
    media_estrelas = serializers.FloatField()
    estrelas_1 = serializers.IntegerField()
    estrelas_2 = serializers.IntegerField()
    estrelas_3 = serializers.IntegerField()
    estrelas_4 = serializers.IntegerField()
    estrelas_5 = serializers.IntegerField()
