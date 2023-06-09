# Generated by Django 4.2.1 on 2023-05-21 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseIng',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ing_name', models.CharField(max_length=200)),
                ('measurement_type', models.CharField(max_length=200)),
                ('package_price', models.FloatField()),
                ('package_size', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_name', models.CharField(max_length=200)),
                ('servings', models.IntegerField()),
                ('descripton', models.TextField()),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIng',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_mass', models.FloatField()),
                ('test', models.FloatField()),
                ('base_ing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calculator.baseing')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calculator.recipe')),
            ],
        ),
    ]
