from django.db import migrations, models
import django.db.models.deletion


RESTAURANTS = [
	('Hearth & Co.', 'hearth-co', 'Contemporary Wood-Fired', 'Soho', '$$$$', 'An outstanding study of dry-aged beef, game bird, and seasonal organic vegetables over open white-oak coals.', 'food1', 4.9),
	('Nori Atelier', 'nori-atelier', 'Modern Japanese Omakase', 'Midtown', '$$$$$', 'Rare seasonal raw fish from small family fisheries in Hokkaido, served at an intimate dining bar.', 'interior', 4.8),
	('Osteria Classica', 'osteria-classica', 'Traditional Northern Italian', 'Brooklyn', '$$', 'Authentic handmade tagliatelle and rich, bone-marrow ragu served in a candlelight-filled cellar.', 'food2', 4.5),
	('Miyako Omakase', 'miyako-omakase', 'Sushi Traditional', 'Midtown', '$$$$', 'A precise omakase menu built around daily arrivals from trusted Japanese fish markets.', 'interior', 4.9),
	("L'Ancora", 'l-ancora', 'Seafood Italian', 'Soho', '$$$', 'Bright coastal cooking with whole fish, handmade pasta, and charred seasonal produce.', 'food1', 4.8),
	('Mercer Brasserie', 'mercer-brasserie', 'French Modern', 'Soho', '$$$', 'Classic French technique meets a lively downtown room and a concise, seasonal menu.', 'food4', 4.6),
	('The Raw Bar Co.', 'the-raw-bar-co', 'Seafood / Oyster Lounge', 'Midtown', '$$$$', 'Native bivalves, hand-harvested kelp, and crisp coastal wines served at the marble counter.', 'food3', 4.7),
	('Juniper Room', 'juniper-room', 'New American', 'Brooklyn', '$$$', 'Ingredient-led plates and thoughtful cocktails in a softly lit neighborhood dining room.', 'food5', 4.6),
	('Cielo Verde', 'cielo-verde', 'Seasonal Vegetables', 'Soho', '$$', 'A generous tasting menu centered on farms within a short drive of the city.', 'food2', 4.5),
	('Bar Aria', 'bar-aria', 'Italian Wine Bar', 'Midtown', '$$', 'Handmade cicchetti, regional pours, and late-night plates in an intimate bar setting.', 'interior', 4.4),
	('Northline Kitchen', 'northline-kitchen', 'Nordic Inspired', 'Brooklyn', '$$$$', 'Clean, restrained cooking that lets wild herbs, grains, and preserved fruit lead.', 'food4', 4.7),
	('Maison Clementine', 'maison-clementine', 'Classic French', 'Soho', '$$$$', 'An elegant dining room for careful sauces, excellent bread, and quietly polished service.', 'food1', 4.8),
]


def seed_catalog(apps, schema_editor):
	Restaurant = apps.get_model('my_one_app', 'Restaurant')
	Review = apps.get_model('my_one_app', 'Review')
	for name, slug, cuisine, location, price, description, image_class, rating in RESTAURANTS:
		restaurant = Restaurant.objects.create(
			name=name, slug=slug, cuisine=cuisine, location=location, price=price,
			description=description, image_class=image_class, rating=rating,
		)
		Review.objects.create(
			restaurant=restaurant, author='Elena Rostova', role='Guest Savora Essayist',
			score=min(float(rating) + 0.5, 10),
			text=f'{name} delivers a thoughtful, memorable meal with a clear point of view.',
		)


class Migration(migrations.Migration):
	initial = True
	dependencies = []
	operations = [
		migrations.CreateModel(
			name='Restaurant',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('name', models.CharField(max_length=120)),
				('slug', models.SlugField(unique=True)),
				('cuisine', models.CharField(max_length=80)),
				('location', models.CharField(max_length=80)),
				('price', models.CharField(max_length=5)),
				('description', models.TextField()),
				('image_class', models.CharField(default='food1', max_length=30)),
				('rating', models.DecimalField(decimal_places=1, default=0, max_digits=2)),
			],
			options={'ordering': ['-rating', 'name']},
		),
		migrations.CreateModel(
			name='Reservation',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('date', models.DateField()),
				('time', models.TimeField()),
				('guests', models.PositiveSmallIntegerField(default=2)),
				('created_at', models.DateTimeField(auto_now_add=True)),
				('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='my_one_app.restaurant')),
			],
			options={'ordering': ['date', 'time']},
		),
		migrations.CreateModel(
			name='Review',
			fields=[
				('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('author', models.CharField(max_length=100)),
				('role', models.CharField(blank=True, max_length=100)),
				('score', models.DecimalField(decimal_places=1, max_digits=3)),
				('text', models.TextField()),
				('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='my_one_app.restaurant')),
			],
		),
		migrations.RunPython(seed_catalog, migrations.RunPython.noop),
	]