#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from apps.users.constants import USER_MSG_SUPERUSER_ERROR


class UserManager(BaseUserManager):

    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        try:
            user = self.get(email=email)
        except User.DoesNotExist:
            user = self.create(email=email, **extra_fields)
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_online', False)
        extra_fields.setdefault('is_verificated', False)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_online', False)
        extra_fields.setdefault('is_verificated', True)

        # Validate the extra fields
        if extra_fields.get('is_staff') is not True:
            raise ValueError(USER_MSG_SUPERUSER_ERROR.format(flag='is_staff'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(USER_MSG_SUPERUSER_ERROR.format(flag='is_superuser'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(USER_MSG_SUPERUSER_ERROR.format(flag='is_active'))
        if extra_fields.get('is_verificated') is not True:
            raise ValueError(USER_MSG_SUPERUSER_ERROR.format(flag='is_verificated'))
        return self._create_user(email, password, first_name, last_name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()

    email = models.EmailField(unique=True, error_messages={'unique': 'The email is already registered'})
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    extra_fields = JSONField(default=dict)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_online = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    recovery_code = models.CharField(blank=True, null=True, default='', max_length=16)
    recovery_attempts = models.IntegerField(blank=True, null=True, default=0)
    activate_code = models.CharField(blank=True, null=True, default='', max_length=16)

    is_online = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verificated = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['first_name']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class ContentTypeApp(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'app'

    def __str__(self):
        return self.name
