from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Group, Lesson, Student, SingleGrade
from .forms import CreateLessonForm, SingleGradeForm, TextFieldForm
from docx import Document
from docx.shared import Inches
from django.urls import reverse
from django.utils import timezone

# Create your views here.


def edit_opinion(request, lvl, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = TextFieldForm(request.POST)
        if form.is_valid():
            student.opinion = form.cleaned_data['text_field']
            student.save()  # Save the student instance to update the opinion field
            # Process or save the text_value here
    else:
        # Pass the current opinion as initial data to the form
        form = TextFieldForm(initial={'text_field': student.opinion})
    return render(request, 'groups/edit_opinion.html', {'form': form})

def delete_grade(request, lvl, pk, pk2):
    student = get_object_or_404(Student, pk=pk)
    grade = get_object_or_404(SingleGrade, pk=pk2)

    if request.method == 'POST':
        grade.delete()
        return redirect(reverse('student_info', args=[lvl, pk]))

    return render(request, 'groups/delete_grade_confirm.html', {'student': student, 'grade': grade})

    
    
def single_grade(request, lvl, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = SingleGradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.save()
            return redirect(reverse('student_info', args=[lvl, pk]))
    else:
    	form = SingleGradeForm()
    	form.fields['student'].initial = student  # Set the initial value for the student field
    	return render(request, 'groups/single_grade.html', {'student':student, 'form':form})

def edit_grade(request, lvl, pk, pk2):
    grade = get_object_or_404(SingleGrade, pk=pk2)
    if request.method == 'POST':
    	form = SingleGradeForm(request.POST, instance=grade)
    	if form.is_valid():
    	    grade = form.save(commit=False)
    	    grade.save()
    	    return redirect(reverse('student_info', args=[lvl, pk]))
    else:
    	form = SingleGradeForm(instance=grade)
    return render(request, 'groups/single_grade.html', {'form':form})


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
    grades = SingleGrade.objects.filter(student=student).order_by('date')
    return render(request, 'groups/student_info.html', {'student':student, 'lessons_absent':lessons_absent, 'group':group, 'grades':grades})

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

