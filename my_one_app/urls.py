from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('restaurants/', views.restaurants, name='restaurants'),
	path('restaurant/', views.restaurant, name='restaurant'),
	path('restaurant/<slug:slug>/', views.restaurant, name='restaurant_detail'),
	path('profile/', views.profile, name='profile'),
	path('article/', views.article, name='article'),
	path('login/', views.login_view, name='login'),
	path('register/', views.register, name='register'),
	path('logout/', views.logout_view, name='logout'),
	path('restaurant/<slug:slug>/favorite/', views.toggle_favorite, name='toggle_favorite'),
	path('restaurant/<slug:slug>/reviews/add/', views.create_review, name='create_review'),
	path('reviews/<int:review_id>/edit/', views.edit_review, name='edit_review'),
	path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
]