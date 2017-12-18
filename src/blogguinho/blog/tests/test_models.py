from django.db import IntegrityError

from django.test import TransactionTestCase

from blog.models import Post


class PostTests(TransactionTestCase):

    def test_str(self):
        post = Post(title='Meu primeiro teste')
        self.assertEquals(str(post), 'Meu primeiro teste')

    def test_unique_slug(self):
        post = Post(title='Post 1', post_slug='post-1')
        post.save()

        post = Post(title='Outro post', post_slug='post-1')

        with self.assertRaises(IntegrityError) as ctx:
            post.save()

        self.assertEqual('UNIQUE constraint failed: blog_post.post_slug',
                         str(ctx.exception))
        count = Post.objects.count()
        self.assertEqual(count, 1)
