from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TableSaloon, Reservation, Menu, Notification, Report, Schedule

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal information', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'role')
    list_filter = ('role',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(TableSaloon)
class TableSaloonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')  
    search_fields = ('name',)  
    list_filter = ('status',)  
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'table_saloon', 'date')  
    search_fields = ('user__email',) 

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  
    search_fields = ('name',)  
    list_filter = ('name',)  

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message')  
    search_fields = ('user__email', 'message')  

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')  
    search_fields = ('user__email',)   

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time')  
    search_fields = ()  