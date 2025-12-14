from django.urls import path
from .views import post_list, profile_view
from . import views

urlpatterns = [
    path('', post_list, name='post_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('post/create/', views.create_post, name='post_create'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', views.post_like, name='post_like'),


]
