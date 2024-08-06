from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, LikeDislike, Profile, Category
from .forms import PostForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import logout

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=post.pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'blog/profile.html', {'user': request.user})

def home(request):
    categories = Category.objects.all()
    return render(request, 'blog/index.html', {'categories': categories})

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts})

@login_required
def create_post(request):
    if not request.user.profile.is_kyc_user:
        return redirect('profile')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'post': post, 'form': form})

@login_required
def like_dislike_post(request, pk, is_like):
    post = get_object_or_404(Post, pk=pk)
    like_dislike, created = LikeDislike.objects.update_or_create(
        post=post, user=request.user,
        defaults={'is_like': is_like},
    )
    return redirect('post_detail', pk=post.pk)

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    likes_count = post.likes_dislikes.filter(is_like=True).count()
    dislikes_count = post.likes_dislikes.filter(is_like=False).count()
    user_has_liked = post.likes_dislikes.filter(user=request.user, is_like=True).exists()
    user_has_disliked = post.likes_dislikes.filter(user=request.user, is_like=False).exists()
    context = {
        'post': post,
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
        'user_has_liked': user_has_liked,
        'user_has_disliked': user_has_disliked,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect('home')

def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})

def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return render(request, 'registration/logout.html')
