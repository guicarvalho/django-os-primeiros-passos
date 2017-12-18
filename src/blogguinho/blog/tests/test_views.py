from django.test import TestCase

from django.urls import reverse

from blog.models import Post


class PostViewTest(TestCase):

    def setUp(self):
        post1 = Post(title='Post 1', content='Postagem de teste 1.', post_slug='post-1')
        post2 = Post(title='Post 2', content='Postagem de teste 1.', post_slug='post-2')
        post3 = Post(title='Post 3', content='Postagem de teste 1.', post_slug='post-3')
        post4 = Post(title='Post 4', content='Postagem de teste 1.', post_slug='post-4')
        post5 = Post(title='Post 5', content='Postagem de teste 1.', post_slug='post-5')
        post6 = Post(title='Post 6', content='Postagem de teste 1.', post_slug='post-6')

        post1.save()
        post2.save()
        post3.save()
        post4.save()
        post5.save()
        post6.save()

    def tearDown(self):
        Post.objects.all().delete()

    def test_index(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post 6')
        self.assertContains(response, 'Post 5')
        self.assertContains(response, 'Post 4')
        self.assertContains(response, 'Post 3')
        self.assertContains(response, 'Post 2')
        self.assertNotContains(response, 'Post 1')

    def test_detail(self):
        response = self.client.get(
            reverse('post-detail', args=('post-1',)))

        post = Post.objects.get(post_slug='post-1')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
