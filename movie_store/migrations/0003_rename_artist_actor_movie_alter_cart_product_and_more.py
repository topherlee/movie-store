# Generated by Django 4.0.4 on 2022-04-29 14:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie_store', '0002_alter_movies_year_released'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Artist',
            new_name='Actor',
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('year_released', models.IntegerField(validators=[django.core.validators.MaxValueValidator(2030), django.core.validators.MinValueValidator(1800)])),
                ('imdb_rating', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('imdb_votes', models.CharField(blank=True, max_length=100)),
                ('metascore', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('runtime', models.IntegerField(blank=True, null=True)),
                ('rating', models.CharField(blank=True, max_length=50, null=True)),
                ('plot_summary', models.TextField(blank=True)),
                ('tagline', models.TextField(blank=True)),
                ('poster_link', models.URLField()),
                ('imdb_link', models.URLField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('actor', models.ManyToManyField(to='movie_store.actor')),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie_store.director')),
                ('genre', models.ManyToManyField(to='movie_store.genre')),
            ],
        ),
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie_store.movie'),
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie_store.movie'),
        ),
        migrations.DeleteModel(
            name='Movies',
        ),
    ]
