from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('photo/<int:photo_id>/edit/', views.edit_photo, name='edit_photo'),
    path('photo/<int:photo_id>/delete/', views.delete_photo, name='delete_photo'),
    path('photo/<int:photo_id>/comment/', views.add_comment, name='add_comment'),
    path('profile/<username>/', views.profile, name='profile'),
]