from django.core.management.base import  BaseCommand
from django.apps import apps
from django.contrib.auth.models import Permission, Group
from apps.users.models import ContentTypeApp
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Crea los permisos de las vistas en todas las aplicaciones del sistema'

    def handle(self, *args, **options):
        for app in apps.get_app_configs():
            if hasattr(app, 'index_name'):
                try:
                    permisos = app.get_permissions_list()
                except AttributeError:
                    pass
                else:
                    for permiso in permisos:
                        instance, created = Permission.objects.get_or_create(
                            content_type=ContentType.objects.get_for_model(ContentTypeApp),
                            name=permiso,
                            codename=permiso
                        )

                        if created:
                            print(f'created permission: {permiso}')

                try:
                    roles = app.get_permissions_dict()
                except AttributeError:
                    pass
                else:
                    for rol in roles:
                        instance, created = Group.objects.get_or_create(
                            name=rol['name']
                        )

                        if created:

                            print(f'created rol: {rol["name"]}')

                            for permiso in rol['permisos']:
                                try:
                                    permiso_rol = Permission.objects.get(name=permiso)
                                except Permission.DoesNotExist:
                                    pass
                                else:
                                    instance.permissions.add(permiso_rol)
