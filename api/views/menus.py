from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from api.models import Menu
from api.serializers import MenuSerializer

class MenuListCreateView(APIView):
    """
    GET: List all menus (accessible to all authenticated users).
    POST: Create a new menu (restricted to Manager/Admin).
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: MenuSerializer(many=True)})
    def get(self, request):
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=MenuSerializer, responses={201: MenuSerializer})
    def post(self, request):
        # Only Manager or Admin can create
        if not request.user.groups.filter(name__in=['Manager', 'Admin']).exists() and not request.user.is_superuser:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuDetailView(APIView):
    """
    GET: Retrieve a menu (accessible to all authenticated users).
    PUT/DELETE: Only Manager/Admin can update or delete.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Menu, pk=pk)

    @swagger_auto_schema(responses={200: MenuSerializer})
    def get(self, request, pk):
        menu = self.get_object(pk)
        serializer = MenuSerializer(menu)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=MenuSerializer, responses={200: MenuSerializer})
    def put(self, request, pk):
        # Only Manager or Admin can update
        if not request.user.groups.filter(name__in=['Manager', 'Admin']).exists() and not request.user.is_superuser:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        menu = self.get_object(pk)
        serializer = MenuSerializer(menu, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        # Only Manager or Admin can delete
        if not request.user.groups.filter(name__in=['Manager', 'Admin']).exists() and not request.user.is_superuser:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        menu = self.get_object(pk)
        menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
