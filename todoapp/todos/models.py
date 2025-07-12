from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.encoding import smart_str as smart_unicode
from django.utils.translation import gettext_lazy as _


class Todo(models.Model):
    """
     Needed fields
        - user (fk to User Model - Use AUTH_USER_MODEL from django.conf.settings)
        - name (max_length=1000)
        - done (boolean with default been false)
        - date_created (with default of creation time)
        - date_completed (set it when done is marked true)

        Add string representation for this model with todos name.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='todos'
    )
    name = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True,blank=True)
  
    @property
    def status(self):
        return 'done' if self.done else 'To do'

    def __str__(self):
        return self.name
    