# Generated by Django 4.1.7 on 2023-05-25 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0031_alter_followup_next_date_alter_notification_lead_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='lead',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='leads.lead'),
        ),
    ]
