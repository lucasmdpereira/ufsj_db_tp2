from django.db import connection
from rest_framework import status, viewsets
from rest_framework.response import Response

from v1.serializers.resumo_de_avaliacoes_serializers import ResumoDeAvaliacoesSerializer


class ResumoDeAvaliacoesViewSet(viewsets.ViewSet):
    
    def create(self, request):
        serializer = ResumoDeAvaliacoesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO resumos_de_avaliacoes (
                        link_google, qtd_avaliacoes, media_estrelas,
                        estrelas_1, estrelas_2, estrelas_3,
                        estrelas_4, estrelas_5
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """, [
                    validated_data['link_google'],
                    validated_data['qtd_avaliacoes'],
                    validated_data['media_estrelas'],
                    validated_data['estrelas_1'],
                    validated_data['estrelas_2'],
                    validated_data['estrelas_3'],
                    validated_data['estrelas_4'],
                    validated_data['estrelas_5']
                ])

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )