# Generated by Django 3.0.3 on 2020-03-08 14:20

from django.db import migrations, models
import explorer.swapi_explorer.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('filename', models.CharField(max_length=36, validators=[explorer.swapi_explorer.models.csv_hash_validator])),
            ],
        ),
    ]
