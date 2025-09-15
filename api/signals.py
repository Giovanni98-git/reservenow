from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def ensure_permissions_and_groups(sender, **kwargs):
    """
    Ensure that the necessary permissions and groups are created after migrations.
    """

    # Permissions for Client
    try:
        view_menu = Permission.objects.get(codename="view_menu")
        add_reservation = Permission.objects.get(codename="add_reservation")
        change_reservation = Permission.objects.get(codename="change_reservation")
        delete_reservation = Permission.objects.get(codename="delete_reservation")
        view_tablesaloon = Permission.objects.get(codename="view_tablesaloon")
        view_schedule = Permission.objects.get(codename="view_schedule")
        
    except Permission.DoesNotExist:
        # If permissions are not found, exit the function
        return

    # === Client's group ===
    client_group, _ = Group.objects.get_or_create(name="Client")
    client_group.permissions.set([
        view_menu,
        add_reservation,
        change_reservation,
        delete_reservation,
        view_tablesaloon,
        view_schedule,
    ])

    # === Manager's group ===
    manager_group, _ = Group.objects.get_or_create(name="Manager")
    manager_group.permissions.set(Permission.objects.all())