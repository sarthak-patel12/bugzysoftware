from django.contrib.auth.decorators import user_passes_test

def check_user(user):
	return not user.is_authenticated
	
user_logout_required = user_passes_test(check_user,'/',None)

def auth_user_shound_not_access(viewfunc):
	return user_passes_test(viewfunc)