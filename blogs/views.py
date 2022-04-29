import sys
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from . models import Blogs, Comments
from django.utils import timezone


# Create your views here.
def home(request):
    blogs_list = Blogs.objects.all()
    context = {"all_blogs": blogs_list}
    return render(request, 'blogs/home.html', context)

def blog_detail(request, blog_id):
    blog_instance = get_object_or_404(Blogs, pk=blog_id)

    # to show all comments to the selected blog
    # blog_comments = Comments.objects.filter(blogs_id=blog_id)
    # blog_comments = blog_instance.comments_set.all()
    blog_comments = blog_instance.related_blog.all()

    context = {
        'blog_instance': blog_instance,
        'blog_comments': blog_comments
    }
    return render(request, 'blogs/blog_details.html', context)

def add_comment(request, blog_id):
    blog_obj = get_object_or_404(Blogs, pk=blog_id)
    try:
        if request.method == 'POST':
            selected_blog = blog_obj.objects.get(pk=request.POST['comments'])
            comment_desc = ""
            commented_at = timezone.now()
            commented_by = "prakash" # for now
        else:
            context = {"error_message" : ""}
            return render(request, 'blogs/home.html', context)
    except:
        context = {"error_message": sys.exc_info()[1].__str__()}
        return render(request, 'blogs/blog_details.html', context)
    else:
        return HttpResponseRedirect(reverse('home'))

def update_blog(request):
    pass