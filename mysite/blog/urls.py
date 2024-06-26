from django.urls import path, re_path
from . import views

#url config
urlpatterns = [
    path('', views.show_article_titles, name='home'),
    path('login/', views.signin_view, name='login'),
    path('register/', views.signup_view, name='register'),
    path('registered/', views.show_registered, name='registered'),
    path('logout/', views.sign_out, name='logout'),
    path('create/', views.create_article_view, name='create'),
    re_path(r'^(?P<slug>[\w-]+)/edit/$', views.show_article_edit, name='article_edit'),
    re_path(r'^(?P<slug>[\w-]+)/$', views.show_article_details, name='article_details')
]