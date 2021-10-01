from django.contrib.auth.base_user import BaseUserManager 
from django.db import models 
from django.contrib.auth.models import AbstractUser
from PIL import Image 

from gdstorage.storage import GoogleDriveStorage
gd_storage = GoogleDriveStorage()

class UserManager(BaseUserManager):
  use_in_migrations = True 
  
  def create_user(self,username,email=None,password=None,**extra_fileds):
    if not username:
      raise ValueError("Username is required")
      
    if not email:
      raise ValueError("email is required")
      
    extra_fileds.setdefault("is_superuser",False)
    extra_fileds.setdefault("is_staff",False)
    email = self.normalize_email(email)
    user = self.model(username=username,email=email,**extra_fileds)
    user.set_password(password)
    user.save(using=self._db)
    return user 
  
  def create_superuser(self,username,email=None,password=None,**extra_fileds):
    if not username:
      raise ValueError("Username required")
    
      
    extra_fileds.setdefault("is_staff",True)
    extra_fileds.setdefault("is_superuser",True)
    
    return self.create_user(username,email,password,**extra_fileds)
    

  
class User(AbstractUser):
  username = models.CharField(max_length=300)
  email = models.EmailField(max_length=200,unique=True)
  photo = models.ImageField(upload_to="userImages/",blank=True,storage=gd_storage)
  info = models.TextField(blank=True)
  full_address = models.CharField(max_length=400,blank=True)
  passion = models.CharField(max_length=150,blank=True)
  
  objects = UserManager()
  EMAIL_FIELD = "email"
  USERNAME_FIELD = "email"
  REQUIRED_FIELDS =["username"]
  
 
       
       
  def __str__(self):
    return self.email
  
 