from django.contrib import admin
from .models import User, TableSaloon, Reservation, Menu, Notification, Report, Schedule

admin.site.register(User)
admin.site.register(TableSaloon)
admin.site.register(Reservation)
admin.site.register(Menu)
admin.site.register(Notification)
admin.site.register(Report)
admin.site.register(Schedule)