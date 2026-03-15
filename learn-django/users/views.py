from django.shortcuts import render
from .models import User

def user_list(request):
    users = User.objects.all()
    return render(request, "users/list.html", {"users": users})

def htmx_list(request):
    return render(request, "users/htmx_list.html")

def user_search(request):
    keyword = request.GET.get("q", "")
    users = User.objects.filter(username__icontains=keyword)

    return render(request, "users/table.html", {"users": users})