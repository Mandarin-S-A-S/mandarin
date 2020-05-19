#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, CreateView, UpdateView, FormView
from django.conf import settings
from braces.views import LoginRequiredMixin, MultiplePermissionsRequiredMixin
from config.utils import convert_dict_breadcrums
from django.urls import reverse
from django.contrib.auth.models import Permission, Group
from .forms import PermissionForm, PermisoDeleteForm, RoleForm, RoleDeleteForm


class ListaRoles(LoginRequiredMixin, MultiplePermissionsRequiredMixin, TemplateView):
    template_name = 'usuarios/roles/lista.pug'
    login_url = settings.LOGIN_URL
    permissions = {
        "all": [
            "users.roles.ver"
        ],
        "crear": [
            "users.roles.ver",
            "users.roles.crear"
        ]
    }

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Roles del sistema'
        kwargs['title_panel'] = 'Listado de roles'
        kwargs['breadcrumbs'] = convert_dict_breadcrums([
            ('Inicio', reverse('index')),
            ('Usuarios', '#'),
            ('Roles', '#'),
        ])
        kwargs['url_datatable'] = reverse('users:rest:lista_roles')
        kwargs['options'] = self.request.user.has_perms(self.permissions.get('crear'))
        kwargs['crear_roles'] = reverse('users:crear_roles')
        return super(ListaRoles,self).get_context_data(**kwargs)


class CreateRoles(LoginRequiredMixin,MultiplePermissionsRequiredMixin,CreateView):
    """
    """
    permissions = {
        "all": [
            "users.roles.ver",
            "users.roles.crear"
        ]
    }
    login_url = settings.LOGIN_URL
    template_name = 'usuarios/roles/crear.pug'
    form_class = RoleForm
    success_url = "../"
    model = Group

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Roles del sistema'
        kwargs['title_panel'] = 'Agregar rol'
        kwargs['breadcrumbs'] = convert_dict_breadcrums([
            ('Inicio', reverse('index')),
            ('Usuarios', '#'),
            ('Roles', reverse('users:lista_roles')),
            ('Crear', '#'),
        ])
        return super(CreateRoles,self).get_context_data(**kwargs)


class UpdateRoles(LoginRequiredMixin,MultiplePermissionsRequiredMixin,UpdateView):
    """
    """
    permissions = {
        "all": [
            "usuarios.roles.ver",
            "usuarios.roles.editar"
        ]
    }
    login_url = settings.LOGIN_URL
    template_name = 'usuarios/roles/editar.pug'
    form_class = RoleForm
    success_url = "../../"
    model = Group

    def dispatch(self, request, *args, **kwargs):
        self.rol = Group.objects.get(id = kwargs['pk'])
        return super(UpdateRoles, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Roles del sistema'
        kwargs['title_panel'] = 'Editar rol'
        kwargs['breadcrumbs'] = convert_dict_breadcrums([
            ('Inicio', reverse('index')),
            ('Usuarios', '#'),
            ('Roles', reverse('users:lista_roles')),
            ('Editar', '#'),
        ])
        return super(UpdateRoles,self).get_context_data(**kwargs)


class DeleteRoles(LoginRequiredMixin, MultiplePermissionsRequiredMixin, FormView):
    template_name = 'usuarios/roles/eliminar.pug'
    login_url = settings.LOGIN_URL
    form_class = RoleDeleteForm
    permissions = {
        "all": [
            "users.roles.ver",
            "users.roles.eliminar"
        ]
    }

    def get_success_url(self):
        return reverse('users:lista_roles')

    def dispatch(self, request, *args, **kwargs):
        self.rol = Group.objects.get(id=kwargs["pk"])
        return super(DeleteRoles, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Roles del sistema'
        kwargs['title_panel'] = 'Eliminar rol'
        kwargs['breadcrumbs'] = convert_dict_breadcrums([
            ('Inicio', reverse('index')),
            ('Usuarios', '#'),
            ('Roles', reverse('users:lista_roles')),
            ('Eliminar', '#')
        ])
        return super(DeleteRoles, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.rol.delete()
        return super(DeleteRoles, self).form_valid(form)

    def get_initial(self):
        return {
            'pk': self.kwargs['pk']
        }


class ListaPermisos(LoginRequiredMixin, MultiplePermissionsRequiredMixin, TemplateView):
    template_name = 'usuarios/permisos/lista.pug'
    login_url = settings.LOGIN_URL
    permissions = {
        "all": [
            "users.permisos.ver"
        ],
        "crear": [
            "users.permisos.ver",
            "users.permisos.crear"
        ]
    }

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Permisos del sistema'
        kwargs['title_panel'] = 'Listado de permisos'
        kwargs['breadcrumbs'] = convert_dict_breadcrums([
            ('Inicio', reverse('index')),
            ('Usuarios', '#'),
            ('Permisos', '#')
        ])
        kwargs['url_datatable'] = reverse('users:rest:lista_permisos')
        kwargs['options'] = self.request.user.has_perms(self.permissions.get('crear'))
        kwargs['crear_permiso'] = reverse('users:crear_permisos')
        return super(ListaPermisos, self).get_context_data(**kwargs)


class CreatePermisos(LoginRequiredMixin, MultiplePermissionsRequiredMixin, CreateView):
    permissions = {
        "all": [
            "users.permisos.ver",
            "users.permisos.crear"
        ]
    }
    login_url = settings.LOGIN_URL
    template_name = 'usuarios/permisos/crear.pug'
    form_class = PermissionForm
    model = Permission

    def get_success_url(self):
        return reverse('users:lista_permisos')

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Permisos del sistema'
        kwargs['title_panel'] = 'Crear permiso'
        kwargs['breadcrumbs'] = convert_dict_breadcrums([
            ('Inicio', reverse('index')),
            ('Usuarios', '#'),
            ('Permisos', reverse('users:lista_permisos')),
            ('Crear', '#')
        ])
        return super(CreatePermisos, self).get_context_data(**kwargs)


class UpdatePermisos(LoginRequiredMixin, MultiplePermissionsRequiredMixin, UpdateView):
    permissions = {
        "all": [
            "users.permisos.ver",
            "users.permisos.editar"
        ]
    }
    login_url = settings.LOGIN_URL
    template_name = 'usuarios/permisos/editar.pug'
    form_class = PermissionForm
    model = Permission
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse('users:lista_permisos')

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Permisos del sistema'
        kwargs['title_panel'] = 'Editar permiso'
        kwargs['breadcrumbs'] = convert_dict_breadcrums([
            ('Inicio', reverse('index')),
            ('Usuarios', '#'),
            ('Permisos', reverse('users:lista_permisos')),
            ('Editar', '#')
        ])
        return super(UpdatePermisos, self).get_context_data(**kwargs)


class DeletePermisos(LoginRequiredMixin, MultiplePermissionsRequiredMixin, FormView):
    template_name = 'usuarios/permisos/eliminar.pug'
    login_url = settings.LOGIN_URL
    form_class = PermisoDeleteForm
    permissions = {
        "all": [
            "users.permisos.ver",
            "users.permisos.eliminar"
        ]
    }

    def get_success_url(self):
        return reverse('users:lista_permisos')

    def dispatch(self, request, *args, **kwargs):
        self.permiso = Permission.objects.get(id=kwargs["pk"])
        return super(DeletePermisos, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Permisos'
        kwargs['title_panel'] = 'Eliminar permiso'
        kwargs['breadcrumbs'] = convert_dict_breadcrums([
            ('Inicio', reverse('index')),
            ('Usuarios', '#'),
            ('Permisos', reverse('users:lista_permisos')),
            ('Eliminar', '#')
        ])
        return super(DeletePermisos, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.permiso.delete()
        return super(DeletePermisos, self).form_valid(form)

    def get_initial(self):
        return {
            'pk': self.kwargs['pk']
        }
