from django.contrib import admin
from  .models import * 
# Register your models her

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display =["username","email","first_name","last_name"]
  
@admin.register(Category)
class CatAdmin(admin.ModelAdmin):
  list_display=["id","title"]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display=["id","author","title","slug","created_at","updated_at","short_description"]
  
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display=["id","user","post","description"]
  
@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
  list_display=["id","user","post","comment","description"]

@admin.register(PostViews)
class PostViewAdmin(admin.ModelAdmin):
  list_display=["id","post","expiry","user_agent"]