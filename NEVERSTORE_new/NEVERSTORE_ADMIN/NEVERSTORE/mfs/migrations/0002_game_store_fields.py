from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mfs", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="image_url",
            field=models.URLField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="game",
            name="is_popular",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="game",
            name="price_currency",
            field=models.CharField(default="USD", max_length=8),
        ),
        migrations.AddField(
            model_name="game",
            name="price_updated_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="game",
            name="steam_app_id",
            field=models.PositiveIntegerField(blank=True, null=True, unique=True),
        ),
    ]
