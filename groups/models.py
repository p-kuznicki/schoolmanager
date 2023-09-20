from django.db import models as ms
from django.utils import timezone

# Create your models here.

class Group(ms.Model):
    """
    Represents a group of students.
    """
    level = ms.CharField(max_length=2, help_text="The level of the group from 0-8, with a letter for different groups of the same lvl  (e.g., '7B').")

    def __str__(self):
        return f"Group {self.level}"


class Student(ms.Model):
    """
    Represents a student.
    """
    name = ms.CharField(max_length=20, help_text="The student's first name.")
    surname = ms.CharField(max_length=20, help_text="The student's last name.")
    group = ms.ForeignKey(Group, on_delete=ms.CASCADE, help_text="The group to which the student belongs.")
  
    def __str__(self):
        return f"{self.surname} {self.name}"

class Lesson(ms.Model):
    """
    Each lesson in a year. Contains date, subject and absencies.
    """
    date = ms.DateField(default= timezone.now)
    subject = ms.CharField(max_length=50, help_text="The subject of the lesson.")
    group = ms.ForeignKey(Group, on_delete=ms.CASCADE, help_text="The group that participated in the lesson.")
    students_present = ms.ManyToManyField(Student, blank=True, related_name='lessons_present')
    students_absent = ms.ManyToManyField(Student, blank=True, related_name='lessons_absent')

    def __str__(self):
        return f"{self.date}: {self.subject}"
