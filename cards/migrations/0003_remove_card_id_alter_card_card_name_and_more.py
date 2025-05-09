# Generated by Django 5.1.7 on 2025-03-30 22:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_card_color_card_flavor_text_card_mana_cost_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='id',
        ),
        migrations.AlterField(
            model_name='card',
            name='card_name',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='card',
            name='flavor_text',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='card',
            name='rules_text',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='card',
            name='stats',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.CreateModel(
            name='CardTyperel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.card')),
            ],
        ),
        migrations.CreateModel(
            name='Subtyperel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_type', models.CharField(max_length=20)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.card')),
            ],
        ),
        migrations.CreateModel(
            name='Supertyperel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.card')),
            ],
        ),
    ]
