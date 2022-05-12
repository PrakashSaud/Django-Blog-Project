import sys
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from . models import Blogs, Comments
from django.utils import timezone
from django.views.generic.edit import UpdateView, DeleteView
from django.core.mail import send_mail, BadHeaderError

from .forms import ContactForm

# import TemplateView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

# Create your views here.
# def home(request):
#     blogs_list = Blogs.objects.all()
#     context = {"all_blogs": blogs_list}
#     return render(request, 'blogs/home.html', context)


class HomeView(TemplateView):
    template_name = "blogs/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs_list'] = Blogs.objects.all()
        return context


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

# class BlogDetailView(DetailView):
#     model = Blogs
#     template_name = 'blogs/blog_details.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


def add_comment(request, blog_id):

    blog_obj = get_object_or_404(Blogs, pk=blog_id)
    try:
        if request.method == 'POST':
            # selected_blog = blog_obj.objects.get(pk=request.POST['comments'])
            selected_blog = blog_obj.get(pk=request.POST['comments'])
            # comment_desc = ""
            # commented_at = timezone.now()
            # commented_by = "prakash" # for now
            context = {'selected_blog': selected_blog}
        else:
            context = {"error_message": ""}
            return render(request, 'blogs/home.html', context)
    except:
        context = {"error_message": sys.exc_info()[1].__str__()}
        return render(request, 'blogs/blog_details.html', context)
    else:
        return HttpResponseRedirect(reverse('blog_detail', args=(selected_blog.id,)))
        # return render(request, 'blogs/blog_details.html', context)


def update_blog(request, blog_id):
    # open a selected blog
    # allow someone to write
    # if he confirm then save the new content but do not allow him to save in database
    # Then return to the home page
    blog_obj = get_object_or_404(Blogs, pk=blog_id)
    pass


class BlogUpdateView(UpdateView):
    pass

# ==========================================

def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            # cc_myself = form.cleaned_data['cc_myself']

            try:
                send_mail(subject, message, sender, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, 'contact.html', {'form': form})


def successView(request):
    return HttpResponse('Success! Thank you for your message.')