from django.urls import path
from . import views

#url config
urlpatterns = [
    path('', views.first_view, name='home'),
    path('login/', views.logged_user, name='login'),
    path('register/', views.signup, name="register"),
    path('registered/', views.show_registered, name="registered")
]