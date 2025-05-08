# v1/views/comentario.py
from django.db import connection
from rest_framework import viewsets, status
from rest_framework.response import Response
from v1.serializers.comentario_serializers import ComentarioSerializer

class ComentarioViewSet(viewsets.ViewSet):
    
    def create(self, request):
        serializer = ComentarioSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO comentarios (
                        data_review_id, link_google, qtd_estrelas,
                        qtd_curtidas, data, texto,
                        usuario_qtd_avaliacoes, usuario_qtd_fotos,
                        usuario_is_local_guide
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """, [
                    serializer.validated_data['data_review_id'],
                    serializer.validated_data['link_google'],
                    serializer.validated_data['qtd_estrelas'],
                    serializer.validated_data['qtd_curtidas'],
                    serializer.validated_data['data'],
                    serializer.validated_data['texto'],
                    serializer.validated_data['usuario_qtd_avaliacoes'],
                    serializer.validated_data['usuario_qtd_fotos'],
                    serializer.validated_data.get('usuario_is_local_guide', False)
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