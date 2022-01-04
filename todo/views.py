from django.shortcuts import render
from .forms import TodoForm
from .models import Todo
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
# Create your views here.

def index(request):
	todos=Todo.objects.all()
	context = {'todos':todos} 
	return render(request,'todo/index.html',context)

def create_todo(request):
	form = TodoForm()
	context = {'form':form}
	print("i am here 1")
	if request.method == "POST":
		print("i am here 2")
		name = request.POST.get('name')
		is_primary = request.POST.get('is_primary',False)

		todo = Todo()
		todo.name = name
		todo.is_primary = True if is_primary == "on" else False
		todo.save()

		return HttpResponseRedirect(reverse("todo_details",kwargs={"user_id":todo.pk}))
	return render(request,'todo/create_todo.html',context)

def todo_details(request, user_id):
	todo = get_object_or_404(Todo,pk=user_id)
	context = {'todo':todo}
	return render(request,'todo/todo-details.html',context)