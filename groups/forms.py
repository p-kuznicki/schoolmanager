
from django import forms
from .models import Lesson, Student, SingleGrade, Group

class TextFieldForm(forms.Form):
    text_field = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

class NameForm(forms.Form):
    name_field = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname_field = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

class SingleGradeForm(forms.ModelForm):
    class Meta:
        model = SingleGrade
        fields = ('student', 'grade', 'description', 'date')

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super(SingleGradeForm, self).__init__(*args, **kwargs)
        if student is not None:
            self.fields['student'].initial = student
            

class CreateLessonForm(forms.ModelForm):
    students_present = forms.ModelMultipleChoiceField(queryset=Student.objects.all(),
            widget=forms.CheckboxSelectMultiple(), required=False,
    )

    class Meta:
        model = Lesson
        fields = ('date', 'subject', 'students_present',)

    def __init__(self, *args, group, initial_present_students=None, **kwargs):
        super().__init__(*args, **kwargs)
        # limit students to those in the current group
        self.fields['students_present'].queryset = Student.objects.filter(group=group)
        if initial_present_students is not None:
            # If there is a saved presence list - use it
            self.fields['students_present'].initial = initial_present_students
        else:
            # If there is no saved presence list - check all students
            self.fields['students_present'].initial = Student.objects.filter(group=group)

