# 06 - Forms
Até o momento estamos fazendo um trabalho bacana, nosso blog já está com uma cara bem agradável e tem uma área administrativa muito útil para cadastrar publicações, mas ainda não temos uma área para que os leitores possam deixar seus comentários. Precisamos criar um formulário com os campos: nome, e-mail e conteúdo.

Django por padrão já possui uma API de formulários, onde podemos aproveitar os nosso modelos para gerar os campos do formulário. Além disso, todas as validações definidas no modelo são passadas para o formulário. Vamos criar o nosso formulário de comentários.

### Criando os testes
Vamos criar dois testes `test_valid_form` e `test_invalid_form`, abra o arquivo `blog/tests/test_forms.py`:
```python
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

    def test_invalid_form(self):
        data = {
            'content': 'Teste de formulario',
            'post_slug': 'post-1'
        }

        form = PostForm(data=data)

        self.assertFalse(form.is_valid())
``` 
Se rodarmos os testes agora eles vão quebrar. Vamos criar a implementação para atender os testes, crie um arquivo `forms.py` dentro da pasta da APP :
```python
# blog/forms.py

from django import forms


from blog.models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'
```
Pronto, mas agora temos um pequeno problema... temos que criar um modelo para o comentário. Altere o arquivo `models.py` e adicione o modelo `Comment`.
```python
class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.TextField()
    post = models.ForeignKey('blog.Post',
                             related_name='comments',
                             on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.email, self.content[:15])
```

> NOTA: Aproveite para praticar, escreva alguns testes para o modelo criado!

Vamos exibir o formulário de comentário na tela de detalhes da postagem, vamos iniciar alterando o arquivo `blog/views.py`.
```python
from django.shortcuts import get_object_or_404, render, redirect

from blog.forms import CommentForm

from blog.models import Post


def index(request):
    last_posts = Post.objects.all().order_by('-created_at')[:5]

    ctx = {'last_posts': last_posts}

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
```
Beleza, agora vamos alterar o arquivo HTML para exibir os comentários e também o formulário para cadastrar um novo comentário. Altere o arquivo `blog/templates/blog/detail.html`.
```html
{% extends 'base.html' %}

{% block title %} {{ post.title }} {% endblock %}

{% block content %}
	<section class="articles">
    <div class="column is-8 is-offset-2">
    	<div class="card article">
		    <div class="card-content">
		      <div class="media">
		        <div class="media-center">
		          <img src="http://www.radfaces.com/images/avatars/baby-sinclair.jpg" class="author-image" alt="Placeholder image">
		        </div>
		        <div class="media-content has-text-centered">
		          <p class="title article-title">{{ post.title }}</p>
		          <p class="subtitle is-6 article-subtitle">
		            <a href="#">@d</a> {{ post.created_at }}
		          </p>
		        </div>
		      </div>

		    	<div class="content article-body">
		        <p>{{ post.content }}</p>
		    	</div>
		  	</div>
			</div>
		</div>
    <div class="column is-8 is-offset-2">
    	<div class="box">
				<h1 class="title">Deixe seu comentário</h1>
				<form action="{% url 'post-detail' post.post_slug %}" method="POST">{% csrf_token %}
					<input type="hidden" id="post_slug" name="post_slaug" value="{{ post.post_slug }}">
	  			{% for field in comment_form %}
  				<div class="field">
					  <label class="label">{{ field.label }}</label>
					  <div class="control">
					    <input
					    	class="input" type="text"
					    	placeholder="{{ field.label }}" 
					    	maxlength="{{ field.field.max_length }}"
								id="{{ field.id_for_label }}"
					    	name="{{ field.html_name }}">

					    	<small style="color:red;">{{field.errors}}</small>
					 	</div>
					</div>
	  			{% endfor %}
	  			<div class="control">
					  <input class="button is-primary" type="submit" value="Salvar">
					</div>
	    	</form>
			</div>

			<!-- COMMENTS -->
			{% for comment in post.comments.all %}
			<div class="box">
			  <article>
			      <div class="content">
			        <p>
			          <strong>{{ comment.name }}</strong> <small>({{ comment.email }})</small>
			          <br>
			          {{ comment.content }}
			        </p>
			      </div>
			  </article>
		  </div>
		  {% endfor %}
		  <!-- END COMMENTS -->

    </div>
  </section>
{% endblock %}
```
Conforme comentado acima conseguimos utilizar os modelos para criar os nossos formulários com as validações necessárias. 

Vamos dar uma olhada com mais calma no conteúdo de `forms.py`, criamos uma classe para representar no nosso formulário `CommentForm` essa classe extende `ModelForm`. Só com isso o Django já sabe que esse formulário será criado com base em um modelo, mas ainda falta dizer para o Django qual é esse modelo.

Então dentro da classe do formulário adicionamos outra classe `Meta`, é nela que vamos informar qual o modelo e também quais são os campos do modelo que devem estar presentes no formulário, isso através dos atributos `model` e `fields` respectivamente.

Faça todas as alterações, e então rode os testes, se tudo estiver OK então rode o servidor e tente escrever um comentário.