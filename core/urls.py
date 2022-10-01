from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('search/',views.search, name='search'),
    path('image/',views.image_search, name='image'),
]
