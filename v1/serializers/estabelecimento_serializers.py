from rest_framework import serializers


class EstabelecimentoSerializer(serializers.Serializer):
    link_google = serializers.CharField(max_length=255)
    categoria = serializers.CharField(max_length=255)
    nome = serializers.CharField(max_length=255)
    endereco = serializers.CharField(max_length=255)
    telefone = serializers.CharField(max_length=255)
    patrocinado = serializers.BooleanField(required=False, default=False)
    website = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=255)