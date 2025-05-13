from django.db import models


class Estabelecimento(models.Model):
    link_google = models.CharField(max_length=255, primary_key=True)
    categoria = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=255)
    patrocinado = models.BooleanField(default=False)
    website = models.CharField(max_length=255)
    
    class Meta:
        managed = False
        db_table = 'estabelecimentos'