from django import forms
from blog.models import BlogPost 
from .models import Comment

# Define a form for creating a new BlogPost
class CreateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image']

# Define a form for updating an existing BlogPost
class UpdateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image']

	def save(self, commit=True):
		# Get the current instance of the BlogPost being updated
		blog_post = self.instance

		# Update the BlogPost instance with the cleaned data from the form
		blog_post.title = self.cleaned_data['title']
		blog_post.body = self.cleaned_data['body']

        # Check if a new image was provided in the form and update the BlogPost's image
		if self.cleaned_data['image']:
			blog_post.image = self.cleaned_data['image']
		# Save the changes to the BlogPost instance in the database if commit is True
		if commit:
			blog_post.save()
		return blog_post
	
# Cross-Site Scripting (XSS) vulnerability
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


