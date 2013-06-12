from django.db import models

from tendenci.apps.dashboard.managers import DashboardStatManager


class DashboardStat(models.Model):
    key = models.CharField(max_length=255)
    value = models.TextField()
    create_dt = models.DateTimeField(auto_now_add=True)

    objects = DashboardStatManager()

    class Meta:
        ordering = ('-create_dt',)
