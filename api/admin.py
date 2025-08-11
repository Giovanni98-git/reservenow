from django.contrib import admin
from .models import User, TableSalon, Reservation, Menu, Notification, Rapport, Horaire

admin.site.register(User)
admin.site.register(TableSalon)
admin.site.register(Reservation)
admin.site.register(Menu)
admin.site.register(Notification)
admin.site.register(Rapport)
admin.site.register(Horaire)