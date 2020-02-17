from django.urls import path
from . import views

app_name = 'tutor'
urlpatterns = [
    path('welcome/', views.ProfileView.as_view(), name = 'welcome'),
]

# To enable viewing images
# Source: https://stackoverflow.com/questions/44386599/image-not-showing-in-django
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)