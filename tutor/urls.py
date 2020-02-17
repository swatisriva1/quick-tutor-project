from django.urls import path
from . import views

app_name = 'quicktutor'
urlpatterns = [
    path('welcome/', views.welcome, name = 'welcome'),
]