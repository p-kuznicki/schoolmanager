from django.shortcuts import render


# Create your views here.

def group_list(request):
    return render(request, 'groups/group_list.html', {})

