from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
import secrets

# Create your models here.
class Navegator(models.Model):
    name = models.CharField(max_length=200)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.mentor.username})'


class Mentorados(models.Model):
    estagio_choices = {
        "E1": '10-100k', # Change Places
        "E2": '10-10k',
    }


    name = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='fotos')
    estagio = models.CharField(max_length=2, choices=estagio_choices)
    token = models.CharField(unique=True, max_length=17)

    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    navegator = models.ForeignKey(Navegator, on_delete=models.CASCADE)

    criado_em = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(16) # pode juntar com um uuid4 e depois rendomisar

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - ({self.mentor})'

class DisponibilidadeHorarios(models.Model):
    data_inicial = models.DateTimeField(null=True, blank=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    agendado = models.BooleanField(default=False)

    @property
    def data_final(self):
        return self.data_inicial + timedelta(minutes=50)
    
    def __str__(self):
        return self.mentor.username
    
class Reuniao(models.Model):
    tag_choices = (
        ('G', 'Gestão'),
        ('M', 'Marketing'),
        ('RH', 'Gestão de pessoas'),
        ('I', 'Impostos')
    )

    data = models.ForeignKey(DisponibilidadeHorarios, on_delete=models.CASCADE)
    mentorado = models.ForeignKey(Mentorados, on_delete=models.CASCADE)
    tag = models.CharField(max_length=2, choices=tag_choices)
    descricao = models.TextField()

class Tarefa(models.Model):
    mentorado = models.ForeignKey(Mentorados, on_delete=models.DO_NOTHING)
    tarefa = models.CharField(max_length=255)
    realizada = models.BooleanField(default=False)


class Upload(models.Model):
    mentorado = models.ForeignKey(Mentorados, on_delete=models.DO_NOTHING)
    video = models.FileField(upload_to='video')