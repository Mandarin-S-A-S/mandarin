from django.apps import AppConfig
from django.urls import reverse


class UsersConfig(AppConfig):
    name = 'apps.users'

    def ready(self):
        self.index_name = 'Usuarios'
        self.icon = 'accessibility'
        self.url = ''
        self.permisos = {
            'users.usuarios'
        }
        self.menu = [
            {
                'name': 'Roles',
                'permiso': 'users.roles',
                'url': reverse('users:lista_roles'),
                'status': '',
                'other_urls': [
                    'users:crear_roles',
                    'users:editar_roles',
                    'users:eliminar_roles',
                ],
                'submenu': []
            },
            {
                'name': 'Permisos',
                'permiso': 'users.permisos',
                'url': reverse('users:lista_permisos'),
                'other_urls': [
                    'users:crear_permisos',
                    'users:editar_permisos',
                    'users:eliminar_permisos',
                ],
                'status': '',
                'submenu': []
            }
        ]

    def get_permissions_list(self):
        lista_permisos = [
            'permisos.ver',
            'permisos.crear',
            'permisos.editar',
            'permisos.eliminar',

            'roles.ver',
            'roles.crear',
            'roles.editar',
        ]
        return lista_permisos

    def get_permissions_dict(self):
        lista_roles = [
            {
                'name': 'Usuarios, ver permisos',
                'permisos': {
                    'permisos.ver'
                }
            },
            {
                'name': 'Usuarios, crear permisos',
                'permisos': {
                    'permisos.ver',
                    'permisos.crear'
                }
            },
            {
                'name': 'Usuarios, editar permisos',
                'permisos': {
                    'permisos.ver',
                    'permisos.editar'
                }
            },
            {
                'name': 'Usuarios, eliminar permisos',
                'permisos': {
                    'permisos.ver',
                    'permisos.eliminar'
                }
            },
            {
                'name': 'Usuarios, total permisos',
                'permisos': {
                    'permisos.ver',
                    'permisos.crear',
                    'permisos.editar',
                    'permisos.eliminar'
                }
            }
        ]
        return lista_roles
