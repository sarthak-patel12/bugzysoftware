"""todosite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo.views import index,create_todo,todo_details,todo_delete,todo_edit
from authentication.views import register,login_user,logout_user,activate_user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name ='home'),
    path('login',login_user, name ='login'),
    path('register',register, name ='register'),
    path('logout_user',logout_user, name ='logout_user'),
    path('create_todo',create_todo, name ='create_todo'),
    path('todo/<user_id>',todo_details, name ='todo_details'),
    path('todo_delete/<user_id>',todo_delete, name ='todo_delete'),
    path('todo_edit/<user_id>',todo_edit, name ='todo_edit'),
    path('activate_user/<uidb64>/<token>',activate_user,name='activate_user'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)