
from django import forms
from .models import Lesson, Student

class CreateLessonForm(forms.ModelForm):
    students_present = forms.ModelMultipleChoiceField(queryset=Student.objects.all(),
            widget=forms.CheckboxSelectMultiple(attrs={"checked":""}), required=False,
    )

    class Meta:
        model = Lesson
        fields = ('date', 'subject', 'students_present',)

    def __init__(self, *args, group, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['students_present'].queryset = Student.objects.filter(group=group)
