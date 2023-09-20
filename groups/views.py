from django.shortcuts import render, get_object_or_404, redirect
from .models import Group, Lesson, Student
from .forms import CreateLessonForm


# Create your views here.

def group_list(request):
    groups = Group.objects.order_by('level')
    return render(request, 'groups/group_list.html', {'groups':groups})

def group_lessons(request, lvl):
    group = get_object_or_404(Group, level=lvl)
    lessons = Lesson.objects.filter(group=group).order_by('-date')
    return render(request, 'groups/group_lessons.html', {'group':group, 'lessons':lessons})

def create_lesson(request, lvl):
    group = get_object_or_404(Group, level=lvl)
    if request.method == 'POST':
        form = CreateLessonForm(request.POST, group=group)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.group = group
            lesson.save()
            students_present= form.cleaned_data['students_present']
            all_students = Student.objects.filter(group=group)
            for student in all_students:
                # Check if the student is present in the form's students_present field
                if student in students_present:
                    # If present, add them to the lesson's students_present field
                     lesson.students_present.add(student)
                else:
                    # If absent, add them to the lesson's students_absent field
                    lesson.students_absent.add(student)
            lesson.save()
            return redirect('group_lessons', lvl=lvl)
    else:
        form = CreateLessonForm(group=group)
    return render(request, 'groups/lesson_edit.html', {'form': form})
