from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TableSaloon, Reservation, Menu, Notification, Report, Schedule

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Fields to be used in displaying the User model.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal information', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # Fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_superuser', 'groups'),
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_superuser')
    list_filter = ( 'is_superuser', 'groups')
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
