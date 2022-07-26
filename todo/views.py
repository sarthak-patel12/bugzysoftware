from django.shortcuts import render
from .forms import TodoForm
from .models import Todo
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
	todos=Todo.objects.filter(owner=request.user)
	context = {'todos':todos} 
	return render(request,'todo/index.html',context)

@login_required
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
		todo.owner = request.user
		files = request.FILES
		todo.profile_pic= files.get('profile_pic')
		todo.save()

		messages.add_message(request,messages.SUCCESS,"Person Created Successfully")
		return HttpResponseRedirect(reverse("todo_details",kwargs={"user_id":todo.pk}))
	return render(request,'todo/create_todo.html',context)

@login_required
def todo_details(request, user_id):
	todo = get_object_or_404(Todo,pk=user_id)
	print(todo.profile_pic.url)
	context = {'todo':todo}
	return render(request,'todo/todo-details.html',context)

def todo_delete(request, user_id):
	todo = get_object_or_404(Todo,pk=user_id)
	context = {'todo':todo}

	if request.method == 'POST':
		if todo.owner == request.user:
			todo.delete()
			messages.add_message(request,messages.SUCCESS,"Person Deleted Successfully")
			return HttpResponseRedirect(reverse('home'))
	return render(request,'todo/todo-delete.html',context)

@login_required
def todo_edit(request, user_id):
	todo = get_object_or_404(Todo,pk=user_id)
	form = TodoForm(instance=todo)
	context = {'todo':todo,'form':form}
	if request.method == "POST":
		if todo.owner == request.user:
			name = request.POST.get('name')
			is_primary = request.POST.get('is_primary',False)

			todo.name = name
			todo.is_primary = True if is_primary == "on" else False
			files = request.FILES
			todo.profile_pic= files.get('profile_pic')
			todo.save()
			messages.add_message(request,messages.SUCCESS,"Person Updated Successfully")
			return HttpResponseRedirect(reverse("todo_details",kwargs={"user_id":todo.pk}))
	return render(request,'todo/todo_edit.html',context)
