from rest_framework.routers import DefaultRouter
from api.views import (
    TableSaloonViewSet, ReservationViewSet,
    NotificationViewSet, ReportViewSet, ScheduleViewSet,
    RegisterView, UserDetailView, UserListView, AdminUpdateRoleView, MenuListCreateView, MenuDetailView
)
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Users
    path('me/', UserDetailView.as_view(), name='user_detail'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/role/', AdminUpdateRoleView.as_view(), name='admin_update_role'),
    
    # Menu 
    path('menus/', MenuListCreateView.as_view(), name='menu-list-create'),
    path('menus/<int:pk>/', MenuDetailView.as_view(), name='menu-detail'),
]

# to be continue
router = DefaultRouter()
router.register('tablesaloons', TableSaloonViewSet)
router.register('reservations', ReservationViewSet)
router.register('notifications', NotificationViewSet)
router.register('reports', ReportViewSet)
router.register('schedules', ScheduleViewSet)

# Combination 
urlpatterns += router.urls