from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate/', views.generate_haiku, name='generate_haiku'),
    path('edit/', views.edit_haiku, name='edit_haiku'),
    path('publish/<int:pk>/', views.publish_haiku, name='publish_haiku'),
]
