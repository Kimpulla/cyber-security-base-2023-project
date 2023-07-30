from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from blog.models import BlogPost

# Cryptographic failure
# Currently stores password as text
""" def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Store the password before calling form.save()
            raw_password = form.cleaned_data.get('password1')
            account = form.save()
            # Set the plaintext password field after saving the form
            account.password_plaintext = raw_password
            account.save()
            email = form.cleaned_data.get('email')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context) """


# Fixed Cryptographic failure
def registration_view(request):

	# Create an empty dictionary to hold context data for the template
	context = {}

	if request.POST:
		# Create a RegistrationForm instance with the submitted data
		form = RegistrationForm(request.POST)

		# Check if the form data is valid
		if form.is_valid():
			# Save the user to the database
			form.save()

			# Retrieve the email and password from the validated data
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')

			# Authenticate the user
			account = authenticate(email=email, password=raw_password)

			# Log the user in
			login(request, account)
			return redirect('home')
		else:
			# If the form data is invalid, add the form to the context to display validation errors
			context['registration_form'] = form

	else:
		# If the request method is not POST, create an empty RegistrationForm
		form = RegistrationForm()
		context['registration_form'] = form
		
	# Render the registration template with the context
	return render(request, 'account/register.html', context)


def logout_view(request):
	logout(request)
	return redirect('/')


def login_view(request):

	context = {}

	user = request.user
	if user.is_authenticated: 
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "account/login.html", context)


def account_view(request):

	if not request.user.is_authenticated:
			return redirect("login")

	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"username": request.POST['username'],
			}
			form.save()
			context['success_message'] = "Updated"
	else:
		form = AccountUpdateForm(

			initial={
					"email": request.user.email, 
					"username": request.user.username,
				}
			)

	context['account_form'] = form

	blog_posts = BlogPost.objects.filter(author=request.user)
	context['blog_posts'] = blog_posts

	return render(request, "account/account.html", context)


def must_authenticate_view(request):
	return render(request, 'account/must_authenticate.html', {})


