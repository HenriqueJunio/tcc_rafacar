# Generated by Django 4.2 on 2023-05-12 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rafacar', '0002_agendamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='nivel',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]