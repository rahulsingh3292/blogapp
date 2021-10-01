from django import forms 
from  .models import User, Post,Comment ,Reply
from django.core.exceptions import ValidationError

class BlogPostForm(forms.ModelForm):
  def clean_title(self):
    title = self.cleaned_data["title"]
    if len(title) < 30:
      raise ValidationError("Title length should be more than 30 characters.")
    return title
 
  def clean_description(self):
    desc = self.cleaned_data["description"]
    if len(desc) < 250:
      raise ValidationError("Post Description should be More than 250 characters.")
    return desc
  
  class Meta:
    model = Post 
    fields = ["title","slug","category","image","description"]

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment 
    fields = ["post","description"]

  
class SignupForm(forms.ModelForm):
  class Meta:
    model = User 
    fields = ["username","email","first_name","last_name","password","photo"]
    


class ReplyForm(forms.ModelForm):
  class Meta:
    model = Reply
    fields = ["post", "comment","description"]

class UpdateProfileForm(forms.ModelForm):
  class Meta:
    model = User 
    fields =["first_name","last_name","photo","info","passion","full_address"]
    