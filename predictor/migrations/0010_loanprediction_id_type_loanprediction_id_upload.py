# Generated by Django 5.0.13 on 2025-06-17 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0009_loanprediction_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanprediction',
            name='id_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='loanprediction',
            name='id_upload',
            field=models.FileField(blank=True, null=True, upload_to='uploaded_ids/'),
        ),
    ]
