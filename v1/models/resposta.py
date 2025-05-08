from django.db import models
from v1.models.comentario import Comentario

class Resposta(models.Model):
    data_review_id = models.ForeignKey(
        Comentario,
        models.CASCADE,
        db_column='data_review_id',
        to_field='data_review_id',
        primary_key=True
    )
    data = models.DateField()
    texto = models.TextField()
    
    class Meta:
        managed = False
        db_table = 'respostas'
