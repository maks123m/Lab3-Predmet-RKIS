from django.urls import path
from .views import post_list, profile_view
from . import views

urlpatterns = [
    path('', post_list, name='post_list'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
