from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('v1', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE estabelecimentos (
                link_google VARCHAR(255) NOT NULL PRIMARY KEY,
                categoria VARCHAR(255) NOT NULL,
                nome VARCHAR(255) NOT NULL,
                endereco VARCHAR(255) NOT NULL,
                telefone VARCHAR(255) NOT NULL,
                patrocinado BOOLEAN NOT NULL DEFAULT FALSE,
                website VARCHAR(255)
            );
            """,
            reverse_sql="""
            DROP TABLE estabelecimentos;
            """
        ),
    ]