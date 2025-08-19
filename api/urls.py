from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, TableSalonViewSet, ReservationViewSet, MenuViewSet, NotificationViewSet, RapportViewSet, HoraireViewSet


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('tablesalons', TableSalonViewSet)
router.register('reservations', ReservationViewSet)
router.register('menus', MenuViewSet)
router.register('notifications', NotificationViewSet)
router.register('rapports', RapportViewSet)
router.register('horaires', HoraireViewSet)

urlpatterns = router.urls