from django.urls import path
from blog.views import (
	create_blog_view,
	detail_blog_view,
	edit_blog_view,
)
# Set the app namespace to 'blog'
app_name = 'blog'

# Define the urlpatterns for the 'blog' app
urlpatterns = [
    # URL pattern for creating a new blog post
    path('create/', create_blog_view, name="create"),

    # URL pattern for viewing a blog post in detail using its slug
    path('<slug>/', detail_blog_view, name="detail"),

    # URL pattern for editing an existing blog post using its slug
    path('<slug>/edit/', edit_blog_view, name="edit"),
 ]


