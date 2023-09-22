from django.urls import path
from . import views

urlpatterns = [
        path('', views.group_list, name='group_list'),
        path('group/<str:lvl>/', views.group_lessons, name='group_lessons'),
        path('group/<str:lvl>/new/', views.create_lesson, name='new_lesson'),
        path('group/<str:lvl>/edit/<int:pk>/', views.edit_lesson, name='edit_lesson'),
        path('group/<str:lvl>/<int:pk>/', views.student_info, name='student_info'),
        path('group/<str:lvl>/status/', views.get_status, name='get_status'),
]
