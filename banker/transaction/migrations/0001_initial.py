# Generated by Django 5.0.4 on 2024-05-07 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_type', models.CharField(choices=[('DEPOSIT', 'DEPOSIT'), ('WITHDRAWAL', 'WITHDRAWAL'), ('TRANSFER', 'TRANSFER')], max_length=20)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('from_account_number', models.CharField(blank=True, max_length=20, null=True)),
                ('to_account_number', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
    ]
