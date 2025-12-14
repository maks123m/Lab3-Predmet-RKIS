from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import RegisterForm, LoginForm, PostForm
from django.http import Http404
from .models import Post
from .forms import CommentForm
from .models import Like
from django.views.decorators.http import require_POST

def register_view(request):
    if request.user.is_authenticated:
        return redirect('post_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = RegisterForm()

    return render(request, 'laba/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('post_list')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('post_list')
    else:
        form = LoginForm()

    return render(request, 'laba/login.html', {'form': form})



@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def post_list(request):
    posts = Post.objects.select_related('author').order_by('-created_at')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'laba/post_list.html',
        {'page_obj': page_obj}
    )

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile

    posts = Post.objects.filter(author=user).order_by('-created_at')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'laba/profile.html',
        {
            'profile_user': user,
            'profile': profile,
            'page_obj': page_obj,
        }
    )

@login_required
def profile_edit(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'laba/profile_edit.html', {'form': form})

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('post_list')

    return redirect('profile', request.user.username)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('profile', username=request.user.username)
    else:
        form = PostForm()

    return render(request, 'laba/post_create.html', {'form': form})

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        raise Http404()

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = PostForm(instance=post)

    return render(request, 'laba/post_edit.html', {'form': form})

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        raise Http404()

    if request.method == 'POST':
        post.delete()
        return redirect('profile', username=request.user.username)

    return redirect('profile', username=request.user.username)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.select_related('author').order_by('created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            raise Http404()

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(
        request,
        'laba/post_detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
        }
    )

@login_required
@require_POST
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like = Like.objects.filter(user=request.user, post=post)

    if like.exists():
        like.delete()
    else:
        Like.objects.create(user=request.user, post=post)

    return redirect(request.META.get('HTTP_REFERER', 'post_list'))
