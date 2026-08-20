from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Additions to django's default user model (username, email, password)
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefon Numarası")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Doğum Tarihi")
    address = models.TextField(blank=True, null=True, verbose_name="Adres")
    
    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'

    def __str__(self):
        return self.username