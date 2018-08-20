from django.urls import path
from . import views
from .views import Home,upload
urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('upload',upload,name='upload'),
]
