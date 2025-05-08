from django.db import models
from v1.models.estabelecimento import Estabelecimento

class ResumoDeAvaliacoes(models.Model):
    link_google = models.ForeignKey(
        Estabelecimento,
        models.CASCADE,
        db_column='link_google',
        to_field='link_google',
        primary_key=True
    )
    qtd_avaliacoes = models.IntegerField()
    media_estrelas = models.FloatField()
    estrelas_1 = models.IntegerField()
    estrelas_2 = models.IntegerField()
    estrelas_3 = models.IntegerField()
    estrelas_4 = models.IntegerField()
    estrelas_5 = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'resumos_de_avaliacoes'