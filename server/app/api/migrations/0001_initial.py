# Generated by Django 5.1.4 on 2025-01-02 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ticker', models.CharField(max_length=10, unique=True)),
                ('quantity', models.IntegerField(default=1)),
                ('buy_price', models.FloatField()),
            ],
        ),
    ]