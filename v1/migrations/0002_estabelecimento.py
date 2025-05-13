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

        migrations.RunSQL(
            sql=[
                "CREATE INDEX idx_estabelecimentos_categoria ON estabelecimentos (categoria);",
                "CREATE INDEX idx_estabelecimentos_nome ON estabelecimentos (nome);",
            ],
            reverse_sql=[
                "DROP INDEX idx_estabelecimentos_categoria ON estabelecimentos;"
                "DROP INDEX idx_estabelecimentos_nome ON estabelecimentos;"
            ]
        ),
    ]