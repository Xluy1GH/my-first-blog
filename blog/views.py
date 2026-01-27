from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    
def post_search(request):
    query = request.GET.get('q', '')
    posts = []

    if query:
        # results = Post.objects.filter(
        #     Q(title__icontains=query) |
        #     Q(text__icontains=query) |
        #     Q(author__icontains=query)
        # )
        user = User.objects.filter(username=query).first()
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(author=user)
            ).order_by('-published_date')

    return render(request, 'blog/post_search.html', {'posts': posts})