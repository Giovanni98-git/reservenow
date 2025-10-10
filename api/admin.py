from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TableSaloon, Reservation

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Champs affichés dans la page de détail
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal information', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # Champs affichés lors de la création d’un utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_superuser', 'groups'),
        }),
    )

    # Liste des colonnes affichées dans la page "Utilisateurs"
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

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
    list_display = ('pk', 'name', 'status')
    search_fields = ('name',)
    list_filter = ('status',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'table_saloon', 'date', 'start', 'end', 'people_count', 'status')
    search_fields = ('user__email',)
