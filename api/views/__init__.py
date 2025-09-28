from .users import (UserListView, UserDetailView, RegisterView, AdminAssignGroupView, CustomTokenObtainPairView ,  UserRetrieveView,
    UserUpdateView,
    UserDeleteView,
    AdminUserActivationView,
    PromoteToSuperuserView,
    PromoteToManagerView,
    DemoteFromManagerView,
    ChangePasswordView,
    DeactivateAccountView )
from .tableSaloons import table_saloon_detail, table_saloons_list
from .reservations import ReservationViewSet
from .menus import MenuDetailView, MenuListCreateView
from .notifications import NotificationViewSet
from .reports import ReportViewSet
from .schedules import ScheduleViewSet