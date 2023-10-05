# Generated by Django 4.2.5 on 2023-10-05 21:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("groups", "0006_singlegrade"),
    ]

    operations = [
        migrations.AddField(
            model_name="singlegrade",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.DeleteModel(
            name="Grading",
        ),
    ]
