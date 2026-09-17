from django.db import models
from django.urls import reverse


class Restaurant(models.Model):
	name = models.CharField(max_length=120)
	slug = models.SlugField(unique=True)
	cuisine = models.CharField(max_length=80)
	location = models.CharField(max_length=80)
	price = models.CharField(max_length=5)
	description = models.TextField()
	image_class = models.CharField(max_length=30, default='food1')
	rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, default=40.7128)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, default=-74.0060)

	class Meta:
		ordering = ['-rating', 'name']

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('restaurant_detail', kwargs={'slug': self.slug})


class Review(models.Model):
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True, related_name='restaurant_reviews')
	author = models.CharField(max_length=100)
	role = models.CharField(max_length=100, blank=True)
	score = models.DecimalField(max_digits=3, decimal_places=1)
	text = models.TextField()

	def __str__(self):
		return f'{self.author} - {self.restaurant.name}'


class Favorite(models.Model):
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='favorite_restaurants')
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='favorites')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['user', 'restaurant'], name='unique_user_restaurant_favorite'),
		]

	def __str__(self):
		return f'{self.user.username} - {self.restaurant.name}'


class Reservation(models.Model):
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reservations')
	date = models.DateField()
	time = models.TimeField()
	guests = models.PositiveSmallIntegerField(default=2)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['date', 'time']

	def __str__(self):
		return f'{self.restaurant.name} - {self.date} {self.time}'
