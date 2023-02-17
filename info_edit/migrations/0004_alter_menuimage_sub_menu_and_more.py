# Generated by Django 4.1.7 on 2023-02-17 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("info_edit", "0003_alter_restaurantmenu_sub_restaurant"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menuimage",
            name="sub_menu",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="MenuImage",
                to="info_edit.restaurantmenu",
            ),
        ),
        migrations.AlterField(
            model_name="restaurantimage",
            name="sub_restaurant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="RestaurantImage",
                to="info_edit.restaurant",
            ),
        ),
    ]
