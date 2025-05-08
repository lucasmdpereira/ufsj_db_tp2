from django.db import models

class Tag(models.Model):
    tag = models.CharField(max_length=255, primary_key=True)
    
    class Meta:
        managed = False
        db_table = 'tags'