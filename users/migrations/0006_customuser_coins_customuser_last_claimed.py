# Generated by Django 5.2.1 on 2025-06-05 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_customuser_avatar"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="coins",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="customuser",
            name="last_claimed",
            field=models.DateField(blank=True, null=True),
        ),
    ]
