# Generated by Django 4.1.7 on 2023-04-08 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0015_alter_lead_a1_alter_lead_age_alter_lead_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='form_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]