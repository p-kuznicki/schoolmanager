from django.urls import path
from . import views

urlpatterns = [
        path('', views.group_list, name='group_list'),
        path('group/<int:pk>/', views.group_lessons, name='group_lessons'),
]
