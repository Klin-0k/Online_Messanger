# Generated by Django 4.2 on 2023-05-01 20:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_message"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="message",
            options={"ordering": ["-created_at"]},
        ),
    ]
