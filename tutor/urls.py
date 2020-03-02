from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'tutor'
urlpatterns = [
    # To enable to view user profle
    path('welcome/', views.ProfileView.as_view(), name = 'welcome'),
    # ex: /tutor/
    path('', views.index, name='index'),
    path('logout/', LogoutView.as_view(template_name='tutor/logout.html'), name='logout'),
    path('tutorprofile/', views.TutorProfileView.as_view(), name='tutor_profile'),
]
