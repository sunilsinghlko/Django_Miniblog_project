from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SignUpForm
from .forms import LoginForm, Postform
from .models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
# Create your views here.


def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        return render(request, 'blog/dashboard.html', {'posts': posts})
    else:
        return HttpResponseRedirect('/login/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Logged in successfully")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')


def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congrats!! You have become an author")
            user=form.save()
            group=Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})


def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Postform(request.POST)
            if form.is_valid():
                form.save()
                form = Postform()
        else:
            form = Postform()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = Postform(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                form=Postform()
        else:
            pi = Post.objects.get(pk=id)
            form = Postform(instance=pi)
        return render(request, 'blog/updatepost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

# Delete Post


def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
