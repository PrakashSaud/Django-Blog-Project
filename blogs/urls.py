from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("<int:blog_id>/", views.blog_detail, name='blog_detail'),
    path("<int:blog_id>/add_comment/", views.add_comment, name='add_comment'),
    path("<int:blog_id>/update_blog/", views.update_blog, name='update_blog'),
]