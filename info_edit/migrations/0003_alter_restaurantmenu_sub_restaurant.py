# Generated by Django 4.1.7 on 2023-02-17 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("info_edit", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="restaurantmenu",
            name="sub_restaurant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Menu",
                to="info_edit.restaurant",
            ),
        ),
    ]
