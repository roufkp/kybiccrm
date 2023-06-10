# Generated by Django 4.1.7 on 2023-05-22 08:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0027_alter_followup_next_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followup',
            name='next_date',
            field=models.DateField(blank=True, default=datetime.date(2023, 5, 23), null=True),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.campaign')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
