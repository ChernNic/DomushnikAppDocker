# Generated by Django 4.2.17 on 2024-12-11 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DomushnikApp', '0010_alter_property_property_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='О себе'),
        ),
    ]