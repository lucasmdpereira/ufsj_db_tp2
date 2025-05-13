from django.db import models


class EstabelecimentoTag(models.Model):
    link_google = models.ForeignKey(
        'Estabelecimento',
        models.CASCADE,
        db_column='link_google',
        to_field='link_google',
        primary_key=True
    )
    tag = models.ForeignKey(
        'Tag',
        models.CASCADE,
        db_column='tag',
        to_field='tag'
    )
    
    class Meta:
        managed = False
        db_table = 'estabelecimento_tags'