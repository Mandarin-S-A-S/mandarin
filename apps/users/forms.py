#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, ButtonHolder, Layout, Div, Row, Column, Fieldset, HTML
from django.contrib.contenttypes.models import ContentType
from .models import ContentTypeApp
from django.contrib.auth.models import Permission, Group
from django.urls import reverse
from crispy_forms.bootstrap import FormActions


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'class': "form-control form-control-lg"})
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Contraseña', 'class': "form-control form-control-lg"})
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            'email',
            'password',
            Div(
                ButtonHolder(
                    Submit('submit', 'Ingresar', css_class='btn btn-success btn-block btn-lg')
                ),
                css_class="login-buttons"
            )
        )


class PermissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)

        self.fields['content_type'].initial = ContentType.objects.get_for_model(ContentTypeApp)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-lg-6 mb-0'),
                Column('codename', css_class='form-group col-lg-6 mb-0'),
                Column('content_type', css_class='d-none')
            ),
            ButtonHolder(
                Submit(
                    'submit',
                    'Guardar',
                    css_class='float-right btn btn-success'
                )
            ),
        )

    class Meta:
        model = Permission
        fields = '__all__'
        labels = {
            'codename': 'Codename'
        }


class PermisoDeleteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PermisoDeleteForm, self).__init__(*args, **kwargs)

        permiso = Permission.objects.get(id=kwargs['initial']['pk'])
        cancel_url = reverse('users:lista_permisos')

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Fieldset(
                'Eliminar permiso: {0}'.format(permiso.codename),
                Row(
                    HTML(
                        """
                        <div><p class="col-lg-12">Estas seguro de realizar esta acción?</p></div>
                        """
                    )
                )
            ),
            Div(
                FormActions(
                    Submit(
                        'submit',
                        'Si, eliminar',
                        css_class='btn btn-danger'
                    ),
                    HTML(
                        """
                        <a href="{0}" class="btn btn-default" role="button">No, cancelar</a>
                        """.format(cancel_url)
                    )
                ),
                css_class='m-l-10'
            )
        )


class RoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        content_type = ContentType.objects.get_for_model(ContentTypeApp)
        exclude_perms = ['add_contenttypeapp', 'change_contenttypeapp', 'delete_contenttypeapp', 'view_contenttypeapp']
        self.fields['permissions'].queryset = Permission.objects.filter(content_type=content_type).exclude(codename__in=exclude_perms)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('name',css_class='form-group col-12 mb-0')
            ),
            Row(
                Column('permissions', css_class='form-group col-12 mb-0')
            ),
            ButtonHolder(
                Submit(
                    'submit',
                    'Guardar',
                    css_class='btn btn-success'
                )
            ),
        )

    class Meta:
        model = Group
        fields = '__all__'


class RoleDeleteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RoleDeleteForm, self).__init__(*args, **kwargs)

        rol = Group.objects.get(id=kwargs['initial']['pk'])
        cancel_url = reverse('users:lista_roles')

        self.helper = FormHelper(self)
        self.helper.layout = Layout(

            Fieldset(
                'Eliminar rol: {0}'.format(rol.name),
                Row(
                    HTML(
                        """
                        <div><p class="col-lg-12">Estas seguro de realizar esta acción?</p></div>
                        """
                    )
                )
            ),
            Div(
                FormActions(
                    Submit(
                        'submit',
                        'Si, eliminar',
                        css_class='btn btn-danger'
                    ),
                    HTML(
                        """
                        <a href="{0}" class="btn btn-default" role="button">No, cancelar</a>
                        """.format(cancel_url)
                    )
                ),
                css_class='m-l-10'
            )
        )
