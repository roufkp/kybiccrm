# Generated by Django 4.1.7 on 2023-05-22 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0028_alter_followup_next_date_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
