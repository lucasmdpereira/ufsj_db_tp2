from django.db import connection
from rest_framework import viewsets, status
from rest_framework.response import Response
from collections import OrderedDict
from v1.serializers.tag_serializers import TagSerializer

class TagViewSet(viewsets.ViewSet):
    
    def create(self, request):
        serializer = TagSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO tags (
                        tag
                    ) VALUES (
                        %s
                    )
                """, [
                    validated_data['tag'],
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