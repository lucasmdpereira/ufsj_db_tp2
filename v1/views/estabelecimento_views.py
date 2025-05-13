from django.db import connection
from rest_framework import status, viewsets
from rest_framework.response import Response

from v1.serializers.estabelecimento_serializers import EstabelecimentoSerializer


class EstabelecimentoView(viewsets.ViewSet):
    def create(self, request):
        serializer = EstabelecimentoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO estabelecimentos (
                        link_google, categoria, nome, 
                        endereco, telefone, patrocinado, website
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s
                    )
                """, [
                    validated_data['link_google'],
                    validated_data['categoria'],
                    validated_data['nome'],
                    validated_data['endereco'],
                    validated_data['telefone'],
                    validated_data.get('patrocinado', False),
                    validated_data.get('website', '')
                ])

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {
                    'error': 'Erro no banco de dados',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )