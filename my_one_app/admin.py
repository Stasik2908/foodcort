from django.contrib import admin
from .models import Favorite, Reservation, Restaurant, Review

admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(Reservation)
admin.site.register(Favorite)
