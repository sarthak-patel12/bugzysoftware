from django.shortcuts import render,redirect
from django.contrib import messages
from validate_email import validate_email
from .models import User
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str,force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading 

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_action_email(user,request):
	current_site = get_current_site(request)
	email_subject = 'Activate your account'
	email_body = render_to_string('authentication/activate.html',{'user':user,'domain':current_site,'uid':urlsafe_base64_encode(force_bytes(user.pk)),'token':generate_token.make_token(user)})
	email = EmailMessage(subject=email_subject, body=email_body,from_email=settings.EMAIL_FROM_USER,to=[user.email])
	EmailThread(email).start()

# Create your views here.
def register(request):
	if request.method == "POST":
		context={'has_error': False,'data':request.POST}
		email = request.POST.get('email')
		username = request.POST.get('username')
		password = request.POST.get('password')
		password2 = request.POST.get('password2')

		if len(password)<6 and password:
			messages.add_message(request,messages.ERROR,'Password should be at least 6 characters')
			context['has_error'] = True

		if password!=password2:
			messages.add_message(request,messages.ERROR,'Password mismatch')
			context['has_error'] = True

		if not validate_email(email) and email:
			messages.add_message(request,messages.ERROR,'Invalid Email ! please enter a valid email')
			context['has_error'] = True

		if not username:
			messages.add_message(request,messages.ERROR,'Username required')
			context['has_error'] = True

		if not email:
			messages.add_message(request,messages.ERROR,'Email required')
			context['has_error'] = True

		if not password:
			messages.add_message(request,messages.ERROR,'Password required')
			context['has_error'] = True

		if not password2:
			messages.add_message(request,messages.ERROR,'Repeat Password required')
			context['has_error'] = True

		if User.objects.filter(username=username).exists() and email:
			messages.add_message(request,messages.ERROR,'Username already exists! Please select another username')
			context['has_error'] = True

		if User.objects.filter(email=email).exists() and username:
			messages.add_message(request,messages.ERROR,'Email already exists! Please select another Email')
			context['has_error'] = True

		if context['has_error']:
			return render(request,'authentication/register.html',context)
		user = User.objects.create_user(username=username,email=email)
		user.set_password(password)
		user.save()

		send_action_email(user,request)

		messages.add_message(request,messages.SUCCESS,'Account Created Successfully, You can now Login, Please verify email before login')
		return redirect('login')
	return render(request,'authentication/register.html')


def login_user(request):
	if request.method == "POST":
		context={'has_error': False,'data':request.POST}
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username=username,password=password)

		if not user.is_email_varifird:
			messages.add_message(request,messages.ERROR,"Email not verified! Please check you email inbox to verify")
			return render(request,'authentication/login.html',context)

		if not user:
			messages.add_message(request,messages.ERROR,"Invalid Credentials")
			return render(request,'authentication/login.html',context)
		login(request,user)
		messages.add_message(request,messages.SUCCESS,f'Welcome {user.username}')
		return redirect(reverse('home'))
	return render(request,'authentication/login.html')


def logout_user(request):
	logout(request)
	messages.add_message(request,messages.SUCCESS,f'Successfully logged out')
	return redirect(reverse('login'))

def activate_user(request,uidb64,token):

	try:
		uid=force_str(urlsafe_base64_decode(uidb64))

		user = User.objects.get(pk=uid)

	except Exception as e:
		user=None 

	if user and generate_token.check_token(user,token):
		user.is_email_varifird=True
		user.save()
		messages.add_message(request,messages.SUCCESS,f'Email Verified, you can now login')
		return redirect(reverse('login'))
	return render(request,'authentication/activat_failed.html',{'user':user})
