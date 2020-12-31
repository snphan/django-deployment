from django.urls import path
from . import views

# TEMPLATE URLS!
app_name = 'basic_app'

urlpatterns = [
    path('register', views.register, name='register'),
    path('', views.index, name='index'),
    path('user_login', views.user_login, name='user_login'),
    path('cats', views.cats, name='cats'),
]