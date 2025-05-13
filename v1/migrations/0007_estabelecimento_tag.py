from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('v1', '0006_tag'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE estabelecimentos_tags (
                link_google VARCHAR(255) NOT NULL,
                tag VARCHAR(255) NOT NULL,
                PRIMARY KEY (link_google, tag),
                CONSTRAINT fk_estab_tag_estabelecimento
                    FOREIGN KEY (link_google)
                    REFERENCES estabelecimentos(link_google)
                    ON DELETE CASCADE,
                CONSTRAINT fk_estab_tag_tag
                    FOREIGN KEY (tag)
                    REFERENCES tags(tag)
                    ON DELETE CASCADE
            );
            """,
            reverse_sql="DROP TABLE estabelecimentos_tags;"
        )
    ]