from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Favorite, Reservation, Restaurant, Review


def home(request):
	return render(request, 'index.html')


def restaurants(request):
	query = request.GET.get('q', '').strip()
	cuisine = request.GET.get('cuisine', '').strip()
	price = request.GET.get('price', '').strip()
	location = request.GET.get('location', '').strip()
	rating = request.GET.get('rating', '').strip()

	queryset = Restaurant.objects.all()
	if query:
		queryset = queryset.filter(Q(name__icontains=query) | Q(cuisine__icontains=query) | Q(location__icontains=query))
	if cuisine:
		queryset = queryset.filter(cuisine__icontains=cuisine)
	if price:
		queryset = queryset.filter(price=price)
	if location:
		queryset = queryset.filter(location__iexact=location)
	if rating:
		try:
			queryset = queryset.filter(rating__gte=float(rating))
		except ValueError:
			rating = ''

	paginator = Paginator(queryset, 3)
	page_obj = paginator.get_page(request.GET.get('page'))
	query_params = request.GET.copy()
	query_params.pop('page', None)
	return render(request, 'restaurants.html', {
		'page_obj': page_obj,
		'filters': {'q': query, 'cuisine': cuisine, 'price': price, 'location': location, 'rating': rating},
		'query_string': query_params.urlencode(),
	})


def restaurant(request, slug='hearth-co'):
	restaurant_obj = get_object_or_404(Restaurant, slug=slug)
	reservation_success = False
	reservation_error = ''
	if request.method == 'POST':
		try:
			guests = int(request.POST.get('guests', 2))
			if guests < 1 or guests > 20:
				raise ValueError
			date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
			time = datetime.strptime(request.POST['time'], '%H:%M').time()
			Reservation.objects.create(
				restaurant=restaurant_obj,
				date=date,
				time=time,
				guests=guests,
			)
			reservation_success = True
		except (KeyError, TypeError, ValueError):
			reservation_error = 'Please choose a valid date, time, and number of guests.'

	return render(request, 'restaurant.html', {
		'restaurant_obj': restaurant_obj,
		'reviews': restaurant_obj.reviews.all(),
		'is_favorite': request.user.is_authenticated and Favorite.objects.filter(user=request.user, restaurant=restaurant_obj).exists(),
		'reservation_success': reservation_success,
		'reservation_error': reservation_error,
	})


@login_required
def toggle_favorite(request, slug):
	restaurant_obj = get_object_or_404(Restaurant, slug=slug)
	if request.method == 'POST':
		favorite, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant_obj)
		if not created:
			favorite.delete()
	return redirect('restaurant_detail', slug=slug)


@login_required
def create_review(request, slug):
	restaurant_obj = get_object_or_404(Restaurant, slug=slug)
	if request.method == 'POST':
		text = request.POST.get('text', '').strip()
		try:
			score = float(request.POST.get('score', '0'))
			if not text or score < 0 or score > 10:
				raise ValueError
			Review.objects.create(restaurant=restaurant_obj, user=request.user, author=request.user.get_full_name() or request.user.username, role='Savora Member', score=score, text=text)
		except (TypeError, ValueError):
			pass
	return redirect('restaurant_detail', slug=slug)


@login_required
def edit_review(request, review_id):
	review = get_object_or_404(Review, id=review_id, user=request.user)
	if request.method == 'POST':
		text = request.POST.get('text', '').strip()
		try:
			score = float(request.POST.get('score', review.score))
			if not text or score < 0 or score > 10:
				raise ValueError
			review.text = text
			review.score = score
			review.save(update_fields=['text', 'score'])
		except (TypeError, ValueError):
			pass
	return redirect('restaurant_detail', slug=review.restaurant.slug)


@login_required
def delete_review(request, review_id):
	review = get_object_or_404(Review, id=review_id, user=request.user)
	slug = review.restaurant.slug
	if request.method == 'POST':
		review.delete()
	return redirect('restaurant_detail', slug=slug)


def login_view(request):
	form = AuthenticationForm(request, data=request.POST or None)
	if request.method == 'POST' and form.is_valid():
		login(request, form.get_user())
		return redirect(request.GET.get('next') or 'profile')
	return render(request, 'registration/login.html', {'form': form})


def register(request):
	form = UserCreationForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		user = form.save()
		login(request, user)
		return redirect('profile')
	return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
	if request.method == 'POST':
		logout(request)
	return redirect('home')


def profile(request):
	return render(request, 'profile.html')


def article(request):
	return render(request, 'article.html')
