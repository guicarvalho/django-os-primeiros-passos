from django.test import TestCase

from blog.forms import PostForm


class PostFormTest(TestCase):

    def test_valid_form(self):
        data = {
            'title': 'Post 1',
            'content': 'Teste de formulario',
            'post_slug': 'post-1'
        }

        form = PostForm(data=data)

        self.assertTrue(form.is_valid())
