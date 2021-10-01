from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.generic import TemplateView,CreateView,UpdateView,DetailView
from gdstorage.storage import GoogleDriveStorage
from django.contrib.auth import (authenticate,login,logout)
from braces.views import AnonymousRequiredMixin
from django.contrib.auth.hashers import make_password 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from  .models import Post,Comment
from  .forms import SignupForm,UpdateProfileForm
from  .extras import * 
from  .models import User 


class SignupView(AnonymousRequiredMixin,CreateView):
  form_class = SignupForm 
  model = User
  template_name = "accounts/signup.html"
  success_url = "/accounts/signup/"
  
  def form_valid(self,form):
    self.username = form.cleaned_data.get("username");
    self.email = form.cleaned_data.get("email")
    if User.objects.filter(email=self.email).exists() or User.objects.filter(username=self.username).exists():
      return JsonResponse({"status":False})
    self.obj  = form.save(commit=False)
    self.obj.is_active = False
    self.obj.password = make_password(self.obj.password)
    self.obj.save()
    send_activation_mail(self.email,self.username)
    return JsonResponse({"status":True})
    
 
  
class LoginView(AnonymousRequiredMixin,TemplateView):
  template_name = "accounts/login.html"
  def post(self,request):
    redirect_url = self.request.POST.get("next")
    email = self.request.POST.get("email")
    password = self.request.POST.get("password")
    user = User.objects.filter(email=email) 
    if user.exists():
      if user.first().is_active == False:
        return JsonResponse({"active":False})
      
    user = authenticate(self.request,email=email,password=password)
    if user is not None:
      login(self.request,user)
      if redirect_url:
        return JsonResponse({"redirect_to":redirect_url})
      return JsonResponse({"status":True})
    return JsonResponse({"status":False})
    



@csrf_exempt
def activate_account(request):
  if request.method == "POST":
    email = request.POST.get("email")
    user = User.objects.filter(email=email).first()
    if user.is_active == False:
        user.is_active = True 
        user.save()
        return JsonResponse({"activated":True})
    else:
      return JsonResponse({"activated":False})
  return render(request,"accounts/activate.html")

  


class UserProfileView (LoginRequiredMixin,TemplateView):
  login_url = "/accounts/login/"
  template_name = "accounts/profile.html"
  
  def get_context_data(self,*args,**kwargs):
    context= super().get_context_data(*args,**kwargs)
    context["user"]= self.request.user
    context["total_comments"] = Comment.objects.filter(user=self.request.user).count()
    context["total_posts"] = Post.objects.filter(author=self.request.user).count();
    return context 
  

class UpdateProfileView(LoginRequiredMixin,UpdateView):
  template_name = "accounts/update_profile.html"
  model = User 
  form_class = UpdateProfileForm
  
  def current_photo(self,**kwargs):
    user= self.model.objects.get(id=self.kwargs.get("pk"))
    if user.photo:
      return user.photo.name
    return None
    
  def form_valid(self,form):
    storage = GoogleDriveStorage()
    img = form.cleaned_data["photo"]
    obj = form.save(commit=False)
    if self.current_photo():
      if img.name != self.current_photo():
        storage.delete(self.current_photo())
    obj.save()
    return redirect("profile")
      

def logout_user(request):
  logout(request)
  return redirect("/")

def forget_email_page(request):
  
  if request.method == "POST":
    email = request.POST.get("email")
    user = User.objects.filter(email=email)
    if user.exists():
      forget_password_mail(email)
      return JsonResponse({"status":True})
    else:
      return JsonResponse({"status":False})
  return render(request,"accounts/forget_email_page.html")


def forget_password(request):
  if request.method == "POST":
    new_pass = request.POST.get("new_pass")
    email = request.POST.get("email")
    
    user = User.objects.get(email=email)
    user.set_password(new_pass)
    user.save()
    
    return JsonResponse({"status":True})
  return render(request,"accounts/forget_password.html")
  