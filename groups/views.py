from django.shortcuts import render, get_object_or_404, redirect
from .models import Group, Lesson
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
        form = CreateLessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.group = group
            lesson.save()
            return redirect('group_lessons', lvl=lvl)
    else:
        form = CreateLessonForm()
    return render(request, 'groups/lesson_edit.html', {'form': form})
