from django.db import migrations

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('v1', '0002_estabelecimento'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE comentarios (
                data_review_id VARCHAR(255) NOT NULL PRIMARY KEY,
                qtd_estrelas INTEGER NOT NULL,
                qtd_curtidas INTEGER NOT NULL,
                data DATE NOT NULL,
                texto LONGTEXT NOT NULL,
                usuario_qtd_avaliacoes INTEGER NOT NULL,
                usuario_qtd_fotos INTEGER NOT NULL,
                usuario_is_local_guide BOOLEAN NOT NULL DEFAULT FALSE
            );
            """,
            reverse_sql="""
            DROP TABLE comentarios;
            """
        ),

        migrations.RunSQL(
            sql=[
                "CREATE INDEX idx_comentarios_data ON comentarios (data);",
                "CREATE INDEX idx_comentarios_estrelas ON comentarios (qtd_estrelas);",
                "CREATE INDEX idx_comentarios_curtidas ON comentarios (qtd_curtidas);"
            ],
            reverse_sql=[
                "DROP INDEX idx_comentarios_data ON comentarios;",
                "DROP INDEX idx_comentarios_estrelas ON comentarios;",
                "DROP INDEX idx_comentarios_curtidas ON comentarios;"
            ]
        ),

        migrations.RunSQL(
            sql="""
            ALTER TABLE comentarios
            ADD COLUMN link_google VARCHAR(255),
            ADD CONSTRAINT fk_estabelecimento
                FOREIGN KEY (link_google) 
                REFERENCES estabelecimentos(link_google)
                ON DELETE CASCADE;
            """,
            reverse_sql="""
            ALTER TABLE comentarios
            DROP FOREIGN KEY fk_estabelecimento,
            DROP COLUMN link_google;
            """
        )
    ]