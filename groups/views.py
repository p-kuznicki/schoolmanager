from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Group, Lesson, Student
from .forms import CreateLessonForm
from docx import Document


# Create your views here.

def group_list(request):
    groups = Group.objects.order_by('level')
    return render(request, 'groups/group_list.html', {'groups':groups})

def group_lessons(request, lvl):
    group = get_object_or_404(Group, level=lvl)
    lessons = Lesson.objects.filter(group=group).order_by('-date')
    students_in = Student.objects.filter(group=group).order_by('surname')
    return render(request, 'groups/group_lessons.html', {'group':group, 'lessons':lessons, 'students_in':students_in})

def student_info(request, lvl, pk):
    student = get_object_or_404(Student, pk=pk)
    lessons_absent = student.lessons_absent.all()
    return render(request, 'groups/student_info.html', {'student':student, 'lessons_absent':lessons_absent})

def get_status(request, lvl):
    group = get_object_or_404(Group, level=lvl)
    lessons = Lesson.objects.filter(group=group).order_by('-date')
    status = Document()
    for lesson in lessons:
        status.add_paragraph(str(lesson))
    response = HttpResponse(content_type='application/msword')
    response['Content-Disposition'] = 'inline; filename="group_status.docx"'
    status.save(response)
    return response 


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

def edit_lesson(request, lvl, pk):
    group = get_object_or_404(Group, level=lvl)
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        form = CreateLessonForm(request.POST, instance=lesson, group=group)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.group = group
            lesson.save()
            students_present= form.cleaned_data['students_present']
            all_students = Student.objects.filter(group=group)
            lesson.students_present.clear()
            lesson.students_absent.clear()
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
        initial_present_students = lesson.students_present.all()
        form = CreateLessonForm(group=group, instance=lesson)
    return render(request, 'groups/lesson_edit.html', {'form': form})

