from django.db import migrations

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('v1', '0003_comentario'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE respostas (
                data_review_id VARCHAR(255) NOT NULL PRIMARY KEY,
                data DATE NOT NULL,
                texto LONGTEXT NOT NULL,
                CONSTRAINT fk_resposta_comentario
                    FOREIGN KEY (data_review_id)
                    REFERENCES comentarios (data_review_id)
                    ON DELETE CASCADE
            );
            """,
            reverse_sql="""
            DROP TABLE respostas;
            """
        ),

        migrations.RunSQL(
            sql=[
                "CREATE INDEX idx_respostas_data ON respostas (data);",
            ],
            reverse_sql=[
                "DROP INDEX idx_respostas_data ON respostas;",
            ]
        ),
    ]