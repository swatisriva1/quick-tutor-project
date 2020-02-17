from django.urls import path

from . import views

app_name = 'tutor'
urlpatterns = [
    # To enable to view user profle
    path('welcome/', views.ProfileView.as_view(), name = 'welcome'),
    # ex: /tutor/
    path('', views.index, name='index'),
]
