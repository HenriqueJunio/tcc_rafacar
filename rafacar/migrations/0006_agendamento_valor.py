# Generated by Django 4.2 on 2023-05-14 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rafacar', '0005_dadospessoais_delete_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='valor',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
