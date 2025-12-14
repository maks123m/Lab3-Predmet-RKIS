from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

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
    profile = request.user.profile  # гарантированно один профиль

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'laba/profile_edit.html', {'form': form})