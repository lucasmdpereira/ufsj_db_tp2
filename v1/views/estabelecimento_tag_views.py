from django.db import connection
from rest_framework import viewsets, status
from rest_framework.response import Response
from v1.serializers.estabelecimento_tag_serializers import EstabelecimentoTagSerializer

class EstabelecimentoTagView(viewsets.ViewSet):
    def create(self, request):
        serializer = EstabelecimentoTagSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        print(validated_data)
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO estabelecimentos_tags (
                        link_google, tag
                    ) VALUES (
                        %s, %s
                    )
                """, [
                    validated_data['link_google'],
                    validated_data['tag'],
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