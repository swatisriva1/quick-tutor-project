from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'tutor'
urlpatterns = [
    # To enable to view user profle
    path('welcome/', views.welcome, name = 'welcome'),
    # ex: /tutor/
    path('', views.index, name='index'),
    path('student/', views.StudentProfileView.as_view(), name = 'student'),
    path('updateinfo/', views.ProfileUpdate.as_view(), name = 'updateinfo'),
    path('tutor/', views.TutorProfileView.as_view(), name = 'tutor'),
    path('logout/', LogoutView.as_view(template_name='tutor/logout.html'), name='logout'),
    path('requesttutor/', views.RequestTutorView.as_view(), name = 'requestTutor'),
]
