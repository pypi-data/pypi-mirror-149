from django.db import models


class Seeding(models.Model):
    name = models.CharField(max_length=128, verbose_name='Name')
    applied = models.DateTimeField(auto_now_add=True, verbose_name='Applied date')

    class Meta:
        verbose_name = 'seeding'
        verbose_name_plural = 'seeding'
        ordering = ('-applied',)
