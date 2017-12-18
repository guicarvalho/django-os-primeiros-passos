from django.db import models


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    post_slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.TextField()
    post = models.ForeignKey('blog.Post',
                             related_name='comments',
                             on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.email, self.content[:15])
