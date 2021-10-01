from django.shortcuts import render,redirect
from gdstorage.storage import GoogleDriveStorage
from django.db.models import Q 
from datetime import timedelta
from django.utils import timezone
from django.views.generic import (View,TemplateView,UpdateView,CreateView,DetailView,ListView)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.http import JsonResponse 
from  .models import (Post,Comment,Category,Reply,PostViews)
from .forms import (BlogPostForm,CommentForm,ReplyForm)
from .extras import paginate

#create your views here..
# authentication and profile view in accounts.py 
def page_not_found_404(request,exception):
  return render(request,"blog/404.html")

class HomeView(TemplateView):
  template_name = "blog/home.html"
  
  def get_context_data(self,*args,**kwargs):
    queryset = Post.objects.order_by("created_at")
    page=self.request.GET.get("page")
    posts = paginate(queryset,5,page)
    context ={"posts":posts}
    return context 
  

  
  
def trending_posts():
  trendings = Post.objects.filter(created_at__gte= timezone.now() - timedelta(days=7)).order_by("-views")
  return trendings
    
class PostDetailView(DetailView):
  template_name = "blog/detail.html"
  model = Post
  def get_context_data(self,*args,**kwargs):
    post = Post.objects.get(slug=self.kwargs["slug"])
    user_agent=self.request.META["HTTP_USER_AGENT"]
    if not PostViews.objects.filter(user_agent=user_agent).filter(post=post).exists():
      PostViews.objects.create(user_agent=user_agent,post=post,expiry= timezone.now() + timedelta(hours=3))
      post.views+=1 
      post.save()
 
    comments = Comment.objects.filter(post__slug=self.kwargs.get("slug"))
    replies = Reply.objects.filter(post__slug=self.kwargs["slug"])
    
    next = Post.objects.order_by("?").exclude(slug=self.kwargs["slug"]).first()
    prev = None
    if next:
      prev = Post.objects.order_by("?").exclude(slug=self.kwargs["slug"]).exclude(slug=next.slug).first()
    
    related = Post.objects.filter(category__title=post.category.title).order_by("?").exclude(slug=post.slug)[0:5]
    trendings= trending_posts()[0:5]
    categories = Category.objects.order_by("?")[0:5]
    
    context = {"comments":comments,"post":post,"replies":replies,"prev":prev,"next":next,"relateds":related,"trendings":trendings,"categories":categories}
    return context

class PostCreateView(LoginRequiredMixin,CreateView):
  login_url = "/accounts/login/"
  template_name = "blog/blogpost.html"
  form_class = BlogPostForm
  
  
  def form_valid(self,form):
    self.obj = form.save(commit=False)
    self.obj.author = self.request.user 
    self.obj.slug = slugify(self.obj.title)
    self.obj.save()
    return self.get_success_url()
    
  def form_invalid(self,form):
    messages.info(self.request,form.errors)
    return redirect(self.request.path)
    
  def get_queryset(self,*args,**kwargs):
    return Post.objects.filter(author=self.request.user)
  
  def get_post_slug(self):
    return self.get_queryset().latest("id").slug
  
  def get_success_url(self,*args,**kwargs):
    return redirect("post_detail",slug=self.get_post_slug())
  
class PostUpdateView(LoginRequiredMixin,UpdateView):
  login_url = "/accounts/login/"
  form_class = BlogPostForm
  template_name = "blog/update_post.html"
  
  def prev_img(self,**kwargs):
    post = Post.objects.get(slug=self.kwargs["slug"])
    return post.image.name
    
  
  def form_valid(self,form):
    img = form.cleaned_data["image"]
    self.obj = form.save(commit=False)
    self.obj.slug = slugify(self.obj.title)
    storage = GoogleDriveStorage()
    if img.name!=self.prev_img():
      storage.delete(self.prev_img())
    self.obj.save()
    return redirect("post_detail",slug=self.obj.slug)
 
  def form_invalid(self,form):
    messages.info(self,request,form.errors)
    return redirect(self.request.path)
  
  def get_queryset(self,**kwargs):
    return Post.objects.filter(slug=self.kwargs["slug"])
  
  
class AddCommentView(CreateView):
  form_class = CommentForm 
  template_name = "blog/detail.html"
  
  
  def form_valid(self,form):
    self.obj = form.save(commit=False)
    self.obj.user = self.request.user
    self.obj.save()
    return JsonResponse({"com":self.latest_comment_by_user()})
    
  def latest_comment_by_user(self,*args,**kwargs):
    comment =Comment.objects.filter(user=self.request.user).latest("id")
    data = {"comment_id":comment.id,"description":comment.description,"user":f"{comment.user.first_name} {comment.user.last_name}","created_at":comment.created_at}
    return data
  
class AddReplyView(CreateView):
  form_class = ReplyForm
  template_name = "blog/detail.html"
  
  def form_valid(self,form):
    self.obj = form.save(commit=False)
    self.obj.user = self.request.user
    self.obj.save()
    return JsonResponse({"status":True,"reply":self.latest_reply_by_user()})
  
  def latest_reply_by_user(self):
    rep = Reply.objects.filter(user=self.request.user).latest("id")
    data = {"comment":f"reply{rep.comment.id}","description":rep.description,"user":f"{rep.user.first_name} {rep.user.last_name}","created_at":rep.created_at}
    return data

def trending_post_page(request):
  trend = trending_posts().order_by("-views")
  page=request.GET.get("page")
  posts = paginate(trend,8,page)
  context ={"posts":posts}
  return render(request,"blog/trendings.html",context)

def category_posts(request):
  title = request.GET.get("category")
  page = request.GET.get("page")
  cat_obj = Post.objects.filter(category__title=title)
  posts = paginate(cat_obj,10,page)
  context ={"posts":posts,"cat":title}
  return render(request,"blog/category.html",context)
  
def delete_views_data(request):
  views = [i for i in PostViews.objects.all()]
  for i in views:
    if timezone.now() >= i.expiry:
      i.delete()
  return JsonResponse({"status":True})

def search_post(request):
  query = request.GET.get("query")
  cat = Post.objects.filter(category__title=query)
  title = Post.objects.filter(title=query)
  author = Post.objects.filter(Q(author__username__contains=query)| Q(author__first_name__contains=query))
  desc = Post.objects.filter(description__contains=query)
  data = title.union(author).union(desc).union(cat)
  page = request.GET.get("page")
  result = paginate(data,10,page)
  return render(request,"blog/search.html",{"posts":result,"showing":query})

def popular_posts(request):
  post = Post.objects.order_by("-views")
  page=request.GET.get("page")
  posts = paginate(post,10,page)
  return render(request,"blog/popular.html",{"posts":posts})

def delete_post(request,id):
  post = Post.objects.get(id=id)
  img_name = post.image.name 
  storage = GoogleDriveStorage()
  storage.delete(img_name)
  post.delete()
  return redirect("/")

def user_all_posts(request):
  if request.user.is_authenticated:
    post = Post.objects.filter(author=request.user)
    page = request.GET.get("page")
    posts = paginate(post,10,page)
    return render(request,"blog/user-posts.html",{"posts":posts})
  return redirect("/")
