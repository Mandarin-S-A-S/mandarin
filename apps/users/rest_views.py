from django_datatables_view.base_datatable_view import BaseDatatableView
from braces.views import MultiplePermissionsRequiredMixin
from .models import ContentTypeApp
from django.db.models import Q
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from apps.utils import render_column_utils


class PermisosListApi(MultiplePermissionsRequiredMixin, BaseDatatableView):
    model = Permission
    columns = ['id', 'name', 'codename', 'content_type']
    order_columns = ['id', 'name', 'codename', 'content_type']
    permissions = {
        "all": [
            "users.permisos"
        ],
        "editar": [
            "users.permisos",
            "users.permisos.editar",
        ],
        "eliminar": [
            "users.permisos",
            "users.permisos.eliminar",
        ]
    }

    def get_initial_queryset(self):
        content_type = ContentType.objects.get_for_model(ContentTypeApp)
        exclude_perms = ['add_contenttypeapp', 'change_contenttypeapp', 'delete_contenttypeapp', 'view_contenttypeapp']
        return Permission.objects.filter(content_type=content_type).exclude(codename__in=exclude_perms)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(name__icontains=search) | Q(codename__icontains=search)
            qs = qs.filter(q)
        return qs

    def render_column(self, row, column):
        if column == 'id':
            permiso = self.request.user.has_perms(self.permissions.get('editar'))
            url = f'editar/{row.id}'
            data_placement = 'right'
            title = f'Editar permiso: {row.name}'
            return render_column_utils.edit_button(permiso=permiso, url=url, data_placement=data_placement, title=title)

        elif column == 'content_type':
            permiso = self.request.user.has_perms(self.permissions.get('eliminar'))
            url = f'eliminar/{row.id}'
            data_placement = 'left'
            title = f'Eliminar permiso: {row.name}'
            return render_column_utils.delete_button(
                permiso=permiso, url=url, data_placement=data_placement, title=title)

        else:
            return super(PermisosListApi, self).render_column(row, column)


class RolesListApi(MultiplePermissionsRequiredMixin, BaseDatatableView):
    model = Group
    columns = ['id', 'name', 'permissions']
    order_columns = ['id', 'name', 'permissions']
    permissions = {
        "all": [
            "users.roles"
        ],
        "editar": [
            "users.roles",
            "users.roles.editar",
        ],
        "eliminar": [
            "users.roles",
            "users.roles.eliminar",
        ]
    }

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(name__icontains=search)
            qs = qs.filter(q)
        return qs

    def render_column(self, row, column):

        if column == 'id':
            permiso = self.request.user.has_perms(self.permissions.get('editar'))
            url = f'editar/{row.id}'
            data_placement = 'right'
            title = f'Editar rol: {row.name}'
            editar = render_column_utils.edit_button_no_div(permiso=permiso, url=url, data_placement=data_placement,
                                                            title=title)

            permiso = self.request.user.has_perms(self.permissions.get('eliminar'))
            url = f'eliminar/{row.id}'
            data_placement = 'right'
            title = f'Eliminar rol: {row.name}'
            eliminar = render_column_utils.delete_button_no_div(permiso=permiso, url=url,
                                                                data_placement=data_placement, title=title)

            return f'<div class="text-center"><span>{editar}</span><span class="ml-2">{eliminar}</span></div>'

        elif column == 'permissions':

            ret = ''

            for permiso in row.permissions.all():
                ret += '<div><span>' + permiso.codename + '</span></div>'

            return ret

        else:
            return super(RolesListApi, self).render_column(row, column)
