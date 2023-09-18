from django.shortcuts import render, get_object_or_404
from .models import Group


# Create your views here.

def group_list(request):
    groups = Group.objects.order_by('level')
    return render(request, 'groups/group_list.html', {'groups':groups})

def group_lessons(request, pk):
    group = get_object_or_404(Group, pk=pk)
    return render(request, 'groups/group_lessons.html', {'group':group})
