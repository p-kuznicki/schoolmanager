from django.urls import path
from . import views

urlpatterns = [
        path('', views.group_list, name='group_list'),
        path('add/', views.add_group, name='add_group'),
        path('<str:lvl>/', views.group_lessons, name='group_lessons'),
        path('<str:lvl>/delete/', views.delete_group, name='delete_group'),
        path('<str:lvl>/new/', views.create_lesson, name='new_lesson'),
        path('<str:lvl>/addstudent/', views.add_student, name='add_student'),
        path('<str:lvl>/edit/<int:pk>/', views.edit_lesson, name='edit_lesson'),
        path('<str:lvl>/delete/<int:pk>/', views.delete_lesson, name='delete_lesson'),
        path('<str:lvl>/<int:pk>/', views.student_info, name='student_info'),
        path('<str:lvl>/<int:pk>/delete', views.delete_student, name='delete_student'),
        path('<str:lvl>/<int:pk>/grade/', views.single_grade, name ='single_grade'),
        path('<str:lvl>/<int:pk>/opinion/', views.edit_opinion, name ='edit_opinion'),
        path('<str:lvl>/<int:pk>/deletegrade/<int:pk2>/', views.delete_grade, name='delete_grade'),
        path('<str:lvl>/<int:pk>/deletenote/<int:pk2>/', views.delete_note, name='delete_note'),
        path('<str:lvl>/<int:pk>/edit/<int:pk2>/', views.edit_grade, name ='edit_grade'),
        path('<str:lvl>/status/', views.get_status, name='get_status'),
        path('<str:lvl>/report/', views.get_report, name='get_report'),
]
