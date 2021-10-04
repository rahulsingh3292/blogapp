from base64 import b64encode 
from django.core.paginator import Paginator 
from django.core.mail import send_mail  
from django.conf import settings 

def encrypt_email(email):
  encode = b64encode(email.encode("utf-8"))
  encrypted = encode.decode("utf-8")
  return encrypted


def paginate(queryset,num,page):
  page_obj = Paginator(queryset,num)
  data = page_obj.get_page(page)
  return data 

def send_activation_mail(email,username):
  to = [email]
  from_mail = settings.EMAIL_HOST_USER
  subject = "Account Activation For Revolve"
  body = f"Hey {username}, Click to the link Activate your Account \n https://revolve-blog.herokuapp.com/accounts/verify-account?email={encrypt_email(email)}"
  send_mail(subject,body,from_mail,to)

def forget_password_mail(email):
  to = [email]
  from_mail = settings.EMAIL_HOST_USER
  subject = "Forget Password"
  body = f" Click The link Reset your password \n https://revolve-blog.herokuapp.com/accounts/forget-password?email={encrypt_email(email)}"
  send_mail(subject,body,from_mail,to)
