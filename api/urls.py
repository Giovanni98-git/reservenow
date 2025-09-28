from rest_framework.routers import DefaultRouter
from api.views import (
    ReservationViewSet,
    NotificationViewSet,
    ReportViewSet,
    ScheduleViewSet,
    RegisterView,
    UserDetailView,
    UserListView,
    UserRetrieveView,
    UserUpdateView,
    UserDeleteView,
    AdminAssignGroupView,
    AdminUserActivationView,
    PromoteToSuperuserView,
    PromoteToManagerView,
    DemoteFromManagerView,
    ChangePasswordView,
    DeactivateAccountView,
    MenuListCreateView,
    MenuDetailView,
    table_saloons_list,
    table_saloon_detail
)
from django.urls import path

from api.views.users import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


# Function-based and class-based API endpoints
urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User management endpoints (current user)
    path('me/', UserDetailView.as_view(), name='user_detail'),
    path('me/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('me/deactivate/', DeactivateAccountView.as_view(), name='deactivate_account'),

    # User management endpoints (admin/managers)
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserRetrieveView.as_view(), name='user_retrieve'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/groups/', AdminAssignGroupView.as_view(), name='admin_assign_groups'),
    path('users/<int:pk>/activation/', AdminUserActivationView.as_view(), name='admin_user_activation'),
    path('users/<int:pk>/promote/superuser/', PromoteToSuperuserView.as_view(), name='promote_to_superuser'),
    path('users/<int:pk>/promote/manager/', PromoteToManagerView.as_view(), name='promote_to_manager'),
    path('users/<int:pk>/demote/manager/', DemoteFromManagerView.as_view(), name='demote_from_manager'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),

    # Menu endpoints
    path('menus/', MenuListCreateView.as_view(), name='menu-list-create'),
    path('menus/<int:pk>/', MenuDetailView.as_view(), name='menu-detail'),

    # TableSaloon endpoints
    path('tablesaloons/', table_saloons_list, name='tablesaloons-list-create'),
    path('tablesaloons/<int:pk>/', table_saloon_detail, name='tablesaloons-detail'),
]

# ViewSets with router
router = DefaultRouter()
router.register('reservations', ReservationViewSet, basename='reservations')
router.register('notifications', NotificationViewSet, basename='notifications')
router.register('reports', ReportViewSet, basename='reports')
router.register('schedules', ScheduleViewSet, basename='schedules')

# Combine router URLs with urlpatterns
urlpatterns += router.urls