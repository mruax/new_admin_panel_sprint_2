# Generated by Django 3.2 on 2023-06-20 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_sql_to_postrges_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(through='movies.GenreFilmwork', to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(related_name='filmworks', through='movies.PersonFilmwork', to='movies.Person'),
        ),
        migrations.AlterUniqueTogether(
            name='genrefilmwork',
            unique_together={('film_work', 'genre')},
        ),
        migrations.AlterUniqueTogether(
            name='personfilmwork',
            unique_together={('film_work', 'person', 'role')},
        ),
    ]
