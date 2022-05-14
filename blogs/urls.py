from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),

    path("", views.HomeView.as_view(), name='home'),
    path("about/", views.AboutView.as_view(), name='about'),
    path("contact/", views.contactView, name='contact'),
    path('success/', views.successView, name='success'),


    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('<int:pk>/publish/', views.blog_publish, name='blog_publish'),
    path('create/', views.CreateBlogView.as_view(), name='blog_create'),
    path('<int:pk>/edit/', views.UpdateBlogView.as_view(), name="blog_update"),
    path('<int:pk>/delete/', views.DeleteBlogView.as_view(), name='blog_delete'),

    path('<int:pk>/comment/add/', views.add_comment_to_blog, name="add_comment"),
    path('<int:pk>/comment/approve/', views.comment_approve, name='comment_remove'),
    path('<int:pk>/comment/remove/', views.comment_remove, name='comment_remove'),

]