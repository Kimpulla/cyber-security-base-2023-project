from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

# Import models and forms from 'blog' and 'account' apps
from blog.models import BlogPost
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account

# Search view is vulnerable to SQL Injection.
# For example: http://127.0.0.1:8000/blog/search/?title=%27%20OR%20%271%27=%271
def search(request):
    title = request.GET.get('title', '')
    # Initially use this flawed line for SQL Injection
    posts = BlogPost.objects.raw('SELECT * FROM blog_blogpost WHERE title LIKE \'%' + title + '%\'')
    return render(request, 'blog/search.html', {'posts': posts})


# View function for creating a new blog post
def create_blog_view(request):

	context = {}
	user = request.user

	# Redirect to a login page if the user is not authenticated
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		form = CreateBlogPostForm()

	context['form'] = form

	return render(request, "blog/create_blog.html", context)

# View function for displaying the details of a blog post
def detail_blog_view(request, slug):

	context = {}
	blog_post = get_object_or_404(BlogPost, slug=slug)
	context['blog_post'] = blog_post
	return render(request, 'blog/detail_blog.html', context)


# View function for editing an existing blog post
def edit_blog_view(request, slug):

	context = {}
	user = request.user

	# Redirect to a login page if the user is not authenticated
	if not user.is_authenticated:
		return redirect("must_authenticate")
	
	blog_post = get_object_or_404(BlogPost, slug=slug)

	# Return an error response if the current user is not the author of the post
	if blog_post.author != user:
		return HttpResponse('You are not the author of that post.')

	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog_post = obj

	form = UpdateBlogPostForm(
			initial = {
					"title": blog_post.title,
					"body": blog_post.body,
					"image": blog_post.image,
			}
		)
	context['form'] = form
	return render(request, 'blog/edit_blog.html', context)

# Function for getting the queryset of blog posts based on search queries
def get_blog_queryset(query=None):
	queryset = []
	queries = query.split(" ")
	for q in queries:
		posts = BlogPost.objects.filter(
				Q(title__icontains=q) | 
				Q(body__icontains=q)
			).distinct()

		for post in posts:
			queryset.append(post)

	return list(set(queryset))	
