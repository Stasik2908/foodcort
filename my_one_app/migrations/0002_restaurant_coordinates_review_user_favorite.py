from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


COORDINATES = {
	'hearth-co': (40.7256, -74.0027),
	'nori-atelier': (40.7580, -73.9855),
	'osteria-classica': (40.6782, -73.9442),
	'miyako-omakase': (40.7614, -73.9776),
	'l-ancora': (40.7218, -74.0007),
	'mercer-brasserie': (40.7233, -74.0020),
	'the-raw-bar-co': (40.7527, -73.9772),
	'juniper-room': (40.7306, -73.9866),
	'cielo-verde': (40.7282, -74.0776),
	'bar-aria': (40.7549, -73.9840),
	'northline-kitchen': (40.6895, -73.9670),
	'maison-clementine': (40.7308, -74.0026),
}


def set_coordinates(apps, schema_editor):
	Restaurant = apps.get_model('my_one_app', 'Restaurant')
	for slug, (latitude, longitude) in COORDINATES.items():
		Restaurant.objects.filter(slug=slug).update(latitude=latitude, longitude=longitude)


class Migration(migrations.Migration):
	dependencies = [
		('my_one_app', '0001_restaurant_review_reservation'),
		migrations.swappable_dependency(settings.AUTH_USER_MODEL),
	]

	operations = [
		migrations.AddField(
			model_name='restaurant',
			name='latitude',
			field=models.DecimalField(decimal_places=6, default=40.7128, max_digits=9),
		),
		migrations.AddField(
			model_name='restaurant',
			name='longitude',
			field=models.DecimalField(decimal_places=6, default=-74.006, max_digits=9),
		),
		migrations.AddField(
			model_name='review',
			name='user',
			field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_reviews', to=settings.AUTH_USER_MODEL),
		),
		migrations.CreateModel(
			name='Favorite',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('created_at', models.DateTimeField(auto_now_add=True)),
				('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='my_one_app.restaurant')),
				('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_restaurants', to=settings.AUTH_USER_MODEL)),
			],
			options={'constraints': [models.UniqueConstraint(fields=('user', 'restaurant'), name='unique_user_restaurant_favorite')]},
		),
		migrations.RunPython(set_coordinates, migrations.RunPython.noop),
	]