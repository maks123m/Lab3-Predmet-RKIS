from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.select_related('author').order_by('-created_at')[:50]
    return render(request, 'laba/post_list.html', {'posts': posts})
