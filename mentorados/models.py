from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Navegator(models.Model):
    name = models.CharField(max_length=200)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Mentorados(models.Model):
    estagio_choices = {
        "E1": '10-100k',
        "E2": '10-10k',
    }


    name = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='uploads/fotos')
    estagio = models.CharField(max_length=2, choices=estagio_choices)

    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    navegator = models.ForeignKey(Navegator, on_delete=models.CASCADE)

    criado_em = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

