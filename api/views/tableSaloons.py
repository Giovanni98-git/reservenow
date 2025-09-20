from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.models import TableSaloon
from api.serializers import TableSaloonSerializer

@swagger_auto_schema(method='GET', responses={200: TableSaloonSerializer(many=True)})
@swagger_auto_schema(method='POST', request_body=TableSaloonSerializer, responses={201: TableSaloonSerializer})
@api_view(['GET', 'POST'])
def table_saloons_list(request):
    """
    GET: List all tables and saloons (accessible to all authenticated users).
    POST: Create a new table/saloon (restricted to Manager/Admin or superuser).
    """
    if request.method == 'GET':
        tables = TableSaloon.objects.all()
        serializer = TableSaloonSerializer(tables, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Only Manager/Admin or superuser can create
        if not request.user.groups.filter(name__in=['Manager']).exists() and not request.user.is_superuser and not request.user.is_authenticated:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = TableSaloonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='GET', responses={200: TableSaloonSerializer})
@swagger_auto_schema(method='PUT', request_body=TableSaloonSerializer, responses={200: TableSaloonSerializer})
@swagger_auto_schema(method='DELETE', responses={204: 'No Content'})
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def table_saloon_detail(request, pk):
    """
    GET: Retrieve table/saloon details (accessible to all authenticated users).
    PUT/DELETE: Only Manager/Admin or superuser can update or delete a table/saloon.
    """
    try:
        table = TableSaloon.objects.get(pk=pk)
    except TableSaloon.DoesNotExist:
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TableSaloonSerializer(table)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not request.user.groups.filter(name__in=['Manager']).exists() and not request.user.is_superuser:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = TableSaloonSerializer(table, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.groups.filter(name__in=['Manager']).exists() and not request.user.is_superuser:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        table.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
