from django.urls import path, include
from .views import ListaPermisos, CreatePermisos, UpdatePermisos, DeletePermisos, ListaRoles, CreateRoles, UpdateRoles, \
    DeleteRoles

app_name = 'users'

urlpatterns = [

    path('roles/', ListaRoles.as_view(), name='lista_roles'),
    path('roles/crear/', CreateRoles.as_view(), name='crear_roles'),
    path('roles/editar/<int:pk>/', UpdateRoles.as_view(), name='editar_roles'),
    path('roles/eliminar/<int:pk>/', DeleteRoles.as_view(), name='eliminar_roles'),

    path('permisos/', ListaPermisos.as_view(), name='lista_permisos'),
    path('permisos/crear/', CreatePermisos.as_view(), name='crear_permisos'),
    path('permisos/editar/<int:pk>/', UpdatePermisos.as_view(), name='editar_permisos'),
    path('permisos/eliminar/<int:pk>/', DeletePermisos.as_view(), name='eliminar_permisos'),

    path('api/v1.0/', include('apps.users.rest_urls', namespace='api_users')),
]
