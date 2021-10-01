from django.db import models
from gdstorage.storage import GoogleDriveStorage
from  .managers import User 
from ckeditor_uploader.fields import RichTextUploadingField 

# Create your models here.
gd_storage = GoogleDriveStorage()


class Category(models.Model):
  title = models.CharField(max_length=200)

  
  def __str__(self):
    return self.title 

class Post(models.Model):
  author = models.ForeignKey(User,on_delete=models.CASCADE)
  title = models.CharField(max_length=300)
  slug = models.SlugField(max_length=800,blank=True)

  views = models.IntegerField(default=1)
  category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="category_post")

  image = models.ImageField(upload_to="postImages/",storage=gd_storage)
  description = RichTextUploadingField()
  created_at = models.DateTimeField(auto_now_add=True, blank=True)
  updated_at = models.DateTimeField(blank=True,null=True)
  
  def __str__(self):
    return self.title
  
  def short_description (self):
    return self.description[0:17]

class Comment(models.Model):
  user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
  post = models.ForeignKey(Post,on_delete=models.CASCADE)
  description = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
  def __str__(self):
    return self.description[0:15]
  
  

class Reply(models.Model):
  comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="comment_replies")
  user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
  post = models.ForeignKey(Post,on_delete=models.CASCADE)
  description = models.TextField()
  created_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
  def __str__(self):
    return self.description[0:16]
  
  
class PostViews(models.Model):
  user_agent = models.CharField(max_length=700)
  post =  models.ForeignKey(Post,on_delete=models.CASCADE)
  expiry = models.DateTimeField()
  
  def __str__(self):
    return self.user_agent
    
  