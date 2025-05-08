from django.db import models
from v1.models.estabelecimento import Estabelecimento

class Comentario(models.Model):
    data_review_id = models.CharField(max_length=255, primary_key=True)
    link_google = models.ForeignKey(
        Estabelecimento,
        models.CASCADE,
        db_column='link_google',
        to_field='link_google'
    )
    qtd_estrelas = models.IntegerField()
    qtd_curtidas = models.IntegerField()
    data = models.DateField()
    texto = models.TextField()
    usuario_qtd_avaliacoes = models.IntegerField()
    usuario_qtd_fotos = models.IntegerField()
    usuario_is_local_guide = models.BooleanField(default=False)
    
    class Meta:
        managed = False
        db_table = 'comentarios'