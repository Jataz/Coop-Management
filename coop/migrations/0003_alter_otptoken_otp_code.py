# Generated by Django 5.0.6 on 2024-07-14 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coop', '0002_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='fbb5ba', max_length=6),
        ),
    ]