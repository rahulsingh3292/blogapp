from django.urls import path 
from  .import views
from  .import accounts
urlpatterns =[
   path("",views.HomeView.as_view(),name="home"),
   
   path("accounts/signup/",accounts.SignupView.as_view(),name="signup"),
   
   path("accounts/verify-account/",accounts.activate_account,name="activate_account"),
   
   path("accounts/logout/",accounts.logout_user,name="logout"),
   
   path("accounts/login/",accounts.LoginView.as_view(),name="login"),
   
   path("accounts/profile/",accounts.UserProfileView.as_view(),name="profile"),
   
   path("accounts/profile-update/<int:pk>/",accounts.UpdateProfileView.as_view(),name="update_profile"),
   
   path("blog/post-detail/<slug:slug>/",views.PostDetailView.as_view(),name="post_detail"),
   
   path("blog/add-comment/",views.AddCommentView.as_view(),name="add_comment"),
   
   path("blog/add-reply/",views.AddReplyView.as_view(),name="reply"),

   
   path("blog/add-post/",views.PostCreateView.as_view(),name="addpost"),
   
   path("blog/update-post/<slug:slug>/",views.PostUpdateView.as_view(),name="update_post"),
   
   path("blog/trendings/",views.trending_post_page,name="trendings"),
   
   path("blog/category/",views.category_posts,name="category_posts"),
   
   path("blog/delete-views/",views.delete_views_data,name="delete_views"),
   
   path('blog/search/',views.search_post,name="search"),
   
   path("blog/popular/",views.popular_posts,name="popular_posts"),
   
   path("blog/user-all-posts/",views.user_all_posts,name="user_posts"),
   
   path("accounts/forget-email-page/",accounts.forget_email_page,name="forget_email_page"),
   
   path("accounts/forget-password/",accounts.forget_password,name="forget_password"),
   
   path("blog/delete/<int:id>/",views.delete_post,name="delete")
   
   
  ]