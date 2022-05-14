import sys
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from . models import Blog, Comment
from django.utils import timezone
from django.views.generic.edit import UpdateView, DeleteView
from django.core.mail import send_mail, BadHeaderError

from .forms import ContactForm, NewUserForm, BlogForm, CommentForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.


class AboutView(generic.TemplateView):
    template_name = 'blogs/about.html'


#==================================================
# Contact


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

# ==========================================

# def home(request):
#     blogs_list = Blogs.objects.all()
#     context = {"all_blogs": blogs_list}
#     return render(request, 'blogs/home.html', context)


class HomeView(generic.ListView):
    model = Blog
    template_name = "blogs/home.html"

    # def get_queryset(self):
    #     return Blog.objects.filter(date_published__lte=timezone.now()).order_by('-date_published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs_list'] = Blog.objects.all()
        return context


# ============================================

#
# def blog_detail(request, blog_id):
#     blog_instance = get_object_or_404(Blog, pk=blog_id)
#
#     # to show all comments to the selected blog
#     # blog_comments = Comments.objects.filter(blogs_id=blog_id)
#     # blog_comments = blog_instance.comments_set.all()
#     blog_comments = blog_instance.related_blog.all()
#
#     context = {
#         'blog_instance': blog_instance,
#         'blog_comments': blog_comments
#     }
#     return render(request, 'blogs/blog_details.html', context)


class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = 'blogs/blog_details.html'


class CreateBlogView(LoginRequiredMixin, generic.CreateView):
    login_url = 'login/'
    model = Blog
    template_name = 'blogs/blog_create_form.html'
    fields = ['title', 'content', 'author']

    def get_success_url(self):
        return reverse('home')


class UpdateBlogView(LoginRequiredMixin, generic.UpdateView):
    login_url = 'login/'
    redirect_field_name = 'blogs/blog_details.html'
    form_class = BlogForm
    model = Blog


class DeleteBlogView(LoginRequiredMixin, generic.DeleteView):
    model = Blog
    success_url = reverse_lazy('post_list')

# ======================================================
# AUTHENTICATION


def register_request(request):
    error_msg = ""
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            error_msg = form.errors
    form = NewUserForm()
    return render(request, 'blogs/register.html', context={"register_form": form, "error_msg": error_msg})


def login_request(request):
    message = ""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                message = "You're now logged In"
                return HttpResponseRedirect(reverse('home'))
            else:
                message = "Invalid Username of Password"
        else:
            message = form.errors

    form = AuthenticationForm()
    return render(request, "blogs/login.html", context={"login_form": form, "message": message})


def logout_request(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

# ===================================================

@login_required
def blog_publish(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.publish()
    return redirect('blog_detail', pk=blog_id)


@login_required()
def add_comment_to_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = CommentForm()
    return render(request, 'blogs/comment_form.html', {'comment_form': form})


@login_required
def comment_approve(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.approve()
    return redirect('blog_detail', pk=comment.blog.pk)


@login_required
def comment_remove(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    blog_pk = comment.blog.pk
    comment.delete()
    return redirect('blog_detail', pk=blog_pk)

