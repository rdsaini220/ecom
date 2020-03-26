from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='bloghome'),
    path('blogpost/<str:id>', views.blogpost, name='blogpost'),
]
