from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import TableSaloon
from api.serializers import TableSaloonSerializer
from api.permissions import IsAdmin

@api_view(['GET', 'POST'])
def table_saloons_list(request):
    if request.method == 'GET':
        tables = TableSaloon.objects.all()
        serializer = TableSaloonSerializer(tables, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Vérification admin
        if not IsAdmin().has_permission(request, table_saloons_list):
            return Response({"detail": "Non autorisé"}, status=status.HTTP_403_FORBIDDEN)
        serializer = TableSaloonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def table_saloon_detail(request, pk):
    try:
        table = TableSaloon.objects.get(pk=pk)
    except TableSaloon.DoesNotExist:
        return Response({"detail": "Not authorized"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TableSaloonSerializer(table)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not IsAdmin().has_permission(request, table_saloon_detail):
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        serializer = TableSaloonSerializer(table, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not IsAdmin().has_permission(request, table_saloon_detail):
            return Response({"detail": "Non autorisé"}, status=status.HTTP_403_FORBIDDEN)
        table.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
