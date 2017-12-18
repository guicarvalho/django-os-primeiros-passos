from django.shortcuts import get_object_or_404, redirect, render

from blog.models import Post

from blog.forms import CommentForm


def index(request):
    last_posts = Post.objects.all().order_by('-created_at')[:5]

    ctx = {
        'last_posts': last_posts
    }

    return render(request, 'blog/index.html', ctx)


def detail(request, post_slug):
    post = get_object_or_404(Post, post_slug=post_slug or request.POST['post_slug'])

    form = CommentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

        return redirect('post-detail', post_slug=comment.post.post_slug)

    ctx = {
        'post': post,
        'comment_form': form,
    }

    return render(request, 'blog/detail.html', ctx)
