from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):
    dependencies = [('mfs', '0002_game_store_fields')]
    operations = [
        migrations.AddField(model_name='game', name='old_price', field=models.DecimalField(decimal_places=2, default=0, max_digits=10)),
        migrations.AddField(model_name='game', name='is_aaa', field=models.BooleanField(default=False)),
        migrations.AddField(model_name='game', name='is_indie', field=models.BooleanField(default=False)),
        migrations.AddField(model_name='game', name='is_free_to_play', field=models.BooleanField(default=False)),
        migrations.CreateModel(
            name='GameRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='ratings', to='mfs.game')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, to='auth.user')),
            ],
            options={'unique_together': {('user', 'game')}},
        ),
    ]
