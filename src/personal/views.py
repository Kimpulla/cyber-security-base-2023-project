from django.shortcuts import render
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Import functions and models from the 'blog' app
from blog.views import get_blog_queryset
from blog.models import BlogPost

# Define the number of blog posts to display per page
BLOG_POSTS_PER_PAGE = 10

# View function for the home screen
def home_screen_view(request, *args, **kwargs):
	
	context = {}

    # Get the search query from the request
	query = ""
	if request.GET:
		query = request.GET.get('q', '')
		context['query'] = str(query)

	# Get the list of blog posts based on the search query, sorted by date_updated in descending order
	blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)
	
	# Pagination
	page = request.GET.get('page', 1)
	blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
	try:
		blog_posts = blog_posts_paginator.page(page)
	except PageNotAnInteger:
		# If the page parameter is not an integer, display the first page
		blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
		
	except EmptyPage:
	# If the page is out of range (e.g., too high), display the last page
		blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

	context['blog_posts'] = blog_posts

    # Render the "personal/home.html" template with the context data
	return render(request, "personal/home.html", context)



