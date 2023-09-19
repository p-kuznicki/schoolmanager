from django.urls import path
from . import views

urlpatterns = [
        path('', views.group_list, name='group_list'),
        path('group/<str:lvl>/', views.group_lessons, name='group_lessons'),
        path('group/<str:lvl>/new/', views.create_lesson, name='new_lesson'),
]
