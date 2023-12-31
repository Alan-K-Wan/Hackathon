# authapp/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'authapp'

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('secret/', views.secret_page, name='secret_page'),
    path('process_input/', views.process_input, name='process_input'),  # Add this line
]
