# Generated by Django 4.2.1 on 2023-06-13 14:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0007_alter_profile_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useraddress",
            name="phone_number",
            field=models.CharField(max_length=10),
        ),
    ]
