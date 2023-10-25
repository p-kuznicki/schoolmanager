from django.urls import path
from . import views

urlpatterns = [
        path('', views.group_list, name='group_list'),
        path('<str:lvl>/', views.group_lessons, name='group_lessons'),
        path('<str:lvl>/new/', views.create_lesson, name='new_lesson'),
        path('<str:lvl>/edit/<int:pk>/', views.edit_lesson, name='edit_lesson'),
        path('<str:lvl>/<int:pk>/', views.student_info, name='student_info'),
        path('<str:lvl>/<int:pk>/grade/', views.single_grade, name ='single_grade'),
        path('<str:lvl>/<int:pk>/edit/<int:pk2>/', views.edit_grade, name ='edit_grade'),
        path('<str:lvl>/status/', views.get_status, name='get_status'),
]
