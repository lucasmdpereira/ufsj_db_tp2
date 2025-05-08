from django.db import migrations

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('v1', '0005_resumo_de_avaliacoes'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE tags (
                tag VARCHAR(255) NOT NULL PRIMARY KEY
            );
            """,
            reverse_sql="""
            DROP TABLE tags;
            """
        ),
        
        migrations.RunSQL(
            sql="CREATE INDEX idx_tags_tag ON tags (tag);",
            reverse_sql="DROP INDEX idx_tags_tag ON tags;"
        )
    ]