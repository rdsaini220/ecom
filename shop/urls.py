from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('tracker/', views.tracker, name='tracker'),
    path('checkout/', views.checkout, name='tracker'),
    path('productView/<int:myid>', views.productView, name='tracker'),
    path('handlerequest/', views.handlerequest, name='handlerequest'),
]
