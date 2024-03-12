from django.urls import path
from . import views

#url config
urlpatterns = [
    path('', views.show_article_titles, name='home'),
    path('login/', views.signin_view, name='login'),
    path('register/', views.signup_view, name="register"),
    path('registered/', views.show_registered, name="registered"),
    path('logout/', views.sign_out, name='logout'),
    path('create/', views.create_article_view, name='create')
]