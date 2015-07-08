# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ValidationError



class Owner(models.Model):
    gen_hash = models.CharField(unique=True, max_length=25, verbose_name='name')
    session_id = models.CharField(max_length=60)


class Link(models.Model):
    link = models.URLField()
    gen_name = models.CharField(max_length=255)
    video_id = models.CharField(max_length=20)
    owner = models.ForeignKey(Owner, related_name='owner')
    img = models.CharField(max_length=100)





