from django.urls import path

from . import views

app_name = 'tutor'
urlpatterns = [
    # ex: /tutor/
    path('', views.index, name='index'),
]