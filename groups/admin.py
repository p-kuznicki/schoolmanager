from django.contrib import admin
from .models import Group, Student, Lesson,SingleGrade

# Register your models here.

admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Lesson)
admin.site.register(SingleGrade)
