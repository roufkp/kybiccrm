# Generated by Django 4.1.7 on 2023-04-08 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0017_lead_source'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='form_id',
            new_name='ad_id',
        ),
    ]