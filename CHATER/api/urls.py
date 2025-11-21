from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    #path('create_chat/', views.create_chat, name='create_chat')
]