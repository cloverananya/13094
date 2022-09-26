from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=255)


class Role(models.Model):
    name = models.CharField(max_length=250)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)


class Property(models.Model):
    name = models.CharField(max_length=250)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Properties'
