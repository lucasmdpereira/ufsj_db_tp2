from rest_framework import serializers


class ComentarioSerializer(serializers.Serializer):
    data_review_id = serializers.CharField(max_length=255)
    link_google = serializers.CharField(max_length=255)
    qtd_estrelas = serializers.IntegerField(min_value=1, max_value=5)
    qtd_curtidas = serializers.IntegerField(min_value=0)
    data = serializers.DateField()
    texto = serializers.CharField()
    usuario_qtd_avaliacoes = serializers.IntegerField(min_value=0)
    usuario_qtd_fotos = serializers.IntegerField(min_value=0)
    usuario_is_local_guide = serializers.BooleanField(default=False)