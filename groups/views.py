from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Group, Lesson, Student, SingleGrade
from .forms import CreateLessonForm, SingleGradeForm
from docx import Document
from docx.shared import Inches


# Create your views here.


def single_grade(request, lvl, pk):
    student = get_object_or_404(Student, pk=pk)
    form = SingleGradeForm()
    form.fields['student'].initial = student  # Set the initial value for the student field
    return render(request, 'groups/single_grade.html', {'student':student, 'form':form})

def group_list(request):
    groups = Group.objects.order_by('level')
    return render(request, 'groups/group_list.html', {'groups':groups})

def group_lessons(request, lvl):
    group = get_object_or_404(Group, level=lvl)
    lessons = Lesson.objects.filter(group=group).order_by('-date')
    students_in = Student.objects.filter(group=group).order_by('surname')
    return render(request, 'groups/group_lessons.html', {'group':group, 'lessons':lessons, 'students_in':students_in})

def student_info(request, lvl, pk):
    group = get_object_or_404(Group, level=lvl)
    student = get_object_or_404(Student, pk=pk)
    lessons_absent = student.lessons_absent.all()
    return render(request, 'groups/student_info.html', {'student':student, 'lessons_absent':lessons_absent, 'group':group})

def get_status(request, lvl):
    group = get_object_or_404(Group, level=lvl)
    lessons = Lesson.objects.filter(group=group).order_by('date')
    status = Document()
    lesson_table = status.add_table(rows=1, cols=3)
    lesson_table.columns[0].width = Inches(0.3)
    lesson_table.columns[1].width = Inches(1.1)
    lesson_table.columns[2].width = Inches(4.6)
    lesson_table.style = 'Table Grid'
    lesson_table.cell(0, 0).text = '#'
    lesson_table.cell(0, 1).text = 'DATE'
    lesson_table.cell(0, 2).text = 'LESSON PLAN'
    row=0
    for lesson in lessons:
        lesson_table.add_row()
        row +=1
        lesson_table.cell(row, 0).text = str(row)
        lesson_table.cell(row, 1).text = str(lesson.date)
        lesson_table.cell(row, 2).text = str(lesson.subject)
    response = HttpResponse(content_type='application/msword')
    response['Content-Disposition'] = f'inline; filename="Status of {group}.docx"'
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

