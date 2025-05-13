from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('v1', '0004_resposta'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE resumos_de_avaliacoes (
                link_google VARCHAR(255) NOT NULL PRIMARY KEY,
                qtd_avaliacoes INTEGER NOT NULL,
                media_estrelas FLOAT NOT NULL,
                estrelas_1 INTEGER NOT NULL,
                estrelas_2 INTEGER NOT NULL,
                estrelas_3 INTEGER NOT NULL,
                estrelas_4 INTEGER NOT NULL,
                estrelas_5 INTEGER NOT NULL,
                CONSTRAINT fk_resumo_estabelecimento
                    FOREIGN KEY (link_google)
                    REFERENCES estabelecimentos(link_google)
                    ON DELETE CASCADE
            );
            """,
            reverse_sql="""
            DROP TABLE resumos_de_avaliacoes;
            """
        ),
    ]