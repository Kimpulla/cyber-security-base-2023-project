from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from account.models import Account


# Function to determine the file path for uploading images
def upload_location(instance, filename):
	file_path = 'blog/{author_id}/{title}-{filename}'.format(
				author_id=str(instance.author.id),title=str(instance.title), filename=filename)
	return file_path

# Model representing a BlogPost
class BlogPost(models.Model):
	title 					= models.CharField(max_length=50, null=False, blank=False)
	body 					= models.TextField(max_length=5000, null=False, blank=False)
	image		 			= models.ImageField(upload_to=upload_location, null=True, blank=True)
	date_published 			= models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated 			= models.DateTimeField(auto_now=True, verbose_name="date updated")
	author 					= models.ForeignKey(Account, on_delete=models.CASCADE, related_name='blog_posts') # Cross-Site Scripting (XSS)
	slug 					= models.SlugField(blank=True, unique=True)

	def __str__(self):
		return self.title

# Signal receiver to delete the associated image file when a BlogPost instance is deleted
@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 
    
# Signal receiver to automatically generate a slug before saving the BlogPost instance
def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username + "-" + instance.title)
		
# Connect the pre_save_blog_post_receiver function to the pre_save signal of the BlogPost model
pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)

# Comments
# Cross-Site Scripting (XSS) vulnerability
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text



