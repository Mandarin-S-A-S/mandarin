#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, FormView, View
from braces.views import LoginRequiredMixin
from django.conf import settings
from config.utils import convert_dict_breadcrums
from .forms import LoginForm
from django.contrib import messages
from apps.users.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect, reverse, redirect


class Login(FormView):

    template_name = 'login.pug'
    form_class = LoginForm

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_verificated:
                login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())
            else:
                messages.warning(self.request, 'El usuario no se encuentra activo')
        else:
            if User.objects.filter(email=email).count() > 0:
                messages.warning(self.request, 'La contraseña no es correcta')
            else:
                messages.info(self.request, 'No existe el usuario')
        return HttpResponseRedirect(self.get_success_url())


class Logout(View):

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect(settings.LOGIN_URL)


class Index(LoginRequiredMixin, TemplateView):

    template_name = 'index.pug'
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):

        kwargs['title'] = 'Dashboard'
        kwargs['breadcrumbs'] = convert_dict_breadcrums([
            ('Home', '#')
        ])
        return super(Index, self).get_context_data(**kwargs)
