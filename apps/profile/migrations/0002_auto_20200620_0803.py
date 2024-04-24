# Generated by Django 2.0 on 2020-06-20 08:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profile", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stripeids",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="stripe_ids",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
