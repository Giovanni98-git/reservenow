from rest_framework.routers import DefaultRouter
from api.views import (
    ReservationViewSet,
    NotificationViewSet,
    ReportViewSet,
    ScheduleViewSet,
    RegisterView,
    UserDetailView,
    UserListView,
    AdminAssignGroupView,
    MenuListCreateView,
    MenuDetailView,
    table_saloons_list,
    table_saloon_detail
)
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Function-based and class-based API endpoints
urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User endpoints
    path('me/', UserDetailView.as_view(), name='user_detail'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/role/', AdminAssignGroupView.as_view(), name='admin_update_role'),

    # Menu endpoints
    path('menus/', MenuListCreateView.as_view(), name='menu-list-create'),
    path('menus/<int:pk>/', MenuDetailView.as_view(), name='menu-detail'),

    # TableSaloon endpoints
    path('tablesaloons/', table_saloons_list, name='tablesaloons-list-create'),
    path('tablesaloons/<int:pk>/', table_saloon_detail, name='tablesaloons-detail'),
]

# ViewSets with router

router = DefaultRouter()
router.register('reservations', ReservationViewSet)
router.register('notifications', NotificationViewSet)
router.register('reports', ReportViewSet)
router.register('schedules', ScheduleViewSet)

# Combine router URLs with urlpatterns
urlpatterns += router.urls
