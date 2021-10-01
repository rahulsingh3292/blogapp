from django.dispatch import receiver 
from django.db.models.signals import post_save,post_delete,pre_save
from  .models import Post,User,Category
  

@receiver(post_delete,sender=Post)
def delete_image_from_gd(sender,instance,**kwargs):
  gd_storage = instance.image.storage 
  
  img = instance.image.name 
  gd_storage.delete(img)

@receiver(post_delete,sender=User)
def delete_user_photo_from_gd(sender,instance,**kwargs):
  if instance.photo:
    gd_storage = instance.photo.storage 
    image = instance.photo.name
    gd_storage.delete(image)
  