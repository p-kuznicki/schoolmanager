
from django import forms
from .models import Lesson

class CreateLessonForm(forms.ModelForm):

    class Meta:
        model = Lesson
        fields = ('date', 'subject',)
