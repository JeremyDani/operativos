from django.urls import path
from .views.login import login_view

urlpatterns = [
    path('login/', login_view, name='api_login'),
]
