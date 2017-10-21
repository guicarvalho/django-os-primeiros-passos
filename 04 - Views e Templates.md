# 04 - Views e Templates
No padrão de projeto MTV *views* são equivalentes a *controllers* do padrão MVC, Django usa MTV como padrão arquitetural.

Para exibir os resultados processados nas *views*, precisamos criar *templates*. Templates são arquivos HTML que recebem os objetos da *view*.

Django é um framework com convenções, e uma delas é que devemos criar uma pasta com o nome de *templates* e dentro de nossas APPs e dentro dessa pasta criamos uma nova pasta com o nome da APP, por exemplo:
```sh
blog
├── admin.py
├── apps.py
├── __init__.py
├── migrations
│   ├── 0001_initial.py
│   ├── __init__.py
├── models.py
├── templates
│   └── blog
├── tests.py
└── views.py
```
No exemplo acima temos a APP blog, dentro de *blog* temos uma pasta *templates* e dentro dela uma pasta *blog*.

## Hello World!
Já fizemos algumas coisas legais com Django, mas chegou a hora de fazer o nosso primeiro Hello World. Conforme conversamos, a *view* é responsável por renderizar o conteúdo para o usuário. Vamos criar um método que retorne o texto `Hello World`.

Abra o arquivo `blog/views.py` e adicione o código a seguir:
```python
from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello World!')
```
Pronto! fizemos o nosso código, mas como podemos acessar a tela para mostrar a mensagem? O Django ainda não sabe para qual *URL* ele deve exibir essa mensagem.

Precisamos fazer o roteamento das funções que estão definidas nas *views* para que o Django possa unir a chamada com a resposta.

Para definir as rotas de sua APP precisamos criar um novo arquivo com o nome de `urls.py` dentro da pasta da APP.
```python
# blog/urls.py

from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]
```
Agora precisamos atualizar o arquivo `urls.py` do projeto.
```python
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls')),
]
```
Agora está tudo pronto, acesse [http://localhost:8000/blog/](http://localhost:8000/blog/), você deve ver a mensagem *Hello World*.

## Criando os testes
Vamos criar as telas de listagem de postagens e a tela de detalhe da postagem. Antes de implementar a funcionalidade, vamos começar escrevendo um testes simples para ambas. Vamos primeiramente organizar os nossos testes em um repositório e seguimentar por arquivos.

Dentro da pasta da APP, crie uma pasta chamada `tests`. Na pasta `tests` crie dois arquivos `test_models.py e test_views.py`. Vamos iniciar com o arquivo `test_models.py`, o conteúdo é o mesmo que temos no arquivo `blog/tests.py`, inclusive lembre-se de apagar esse arquivo:
```python
# blog/tests/test_models.py

from django.test import TestCase

from blog.models import Post


class PostTests(TestCase):

    def test_str(self):
        post = Post(title='Meu primeiro teste')
        self.assertEquals(str(post), 'Meu primeiro teste')
```
Nesse arquivo vamos colocar todos os testes relacionados aos modelos da nossa aplicação.

Agora vamos editar o arquivo `test_views.py`, seu objetivo é centralizar todos os testes de `views` da app.
```python
# blog/tests/test_views.py
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
```

## Listando as postagens
Vamos criar a página *home* do nosso blog, onde vamos exibir os últimos 5 posts publicados. Vamos alterar o código da função `index`:
```python
from django.shortcuts import render

from blog.models import Post


def index(request):
    last_posts = Post.objects.all().order_by('-created_at')[:5]

    ctx = {
        'last_posts': last_posts
    }

    return render(request, 'blog/index.html', ctx)
```
No código acima primeiro recuperamos os 5 últimos posts em ordem decrescente, ordenados pela data de criação.

Depois criamos um dicionário com a chave `last_posts`, esse dicionário armazena os valores que serão enviados ao *template* pela *view*.

E por fim, utilizamos o atalho *render* para renderizar o *template* `index.html`, passando os valores definidos no dicionário para o *template*.

## Criando os templates
Vamos criar os templates necessários para exibir nossas postagens. Existe uma convenção onde criamos um template *base*, nesse *template base* importamos nossas bibliotecas *CSS e JS* que serão usadas nos templates.

Crie uma pasta chamada *templates* na pasta raíz do projeto. Nessa pasta vamos criar o arquivo `base.html` com o seguinte conteúdo:
```html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Blogguinho - {% block title %}{% endblock %}</title>
</head>
<body>
	{% block content %}
	{% endblock %}
</body>
</html>
```
Agora temos que informar ao Django que ele deve buscar os *templates* nessa pasta também. Por padrão o Django irá buscar por *templates* em todas as APP's, na prática ele lê o diretório e busca uma pasta chamada *templates*. Abra o arquivo `settings.py` e procure por TEMPLATES, e então altere o valor de DIRS:
```python
'DIRS': [os.path.join(BASE_DIR, 'templates')]
```
No final você deve ter algo parecido com:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
#### base.html
`templates/base.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Blogguinho - {% block title %}{% endblock %}</title>
</head>
<body>
	{% block content %}
	{% endblock %}
</body>
</html>
```
#### index.html
`blog/templates/blog/index.html`
```html
{% extends 'base.html' %}

{% block title %} Últimas postagens {% endblock %}

{% block content %}
	<section id="last-posts">
		<header>
			<h1>Últimas postagens</h1>
		</header>
	{% for post in last_posts %}
			<article>
				<h1>{{ post.title }}</h1>
				<em>{{ post.created_at }}</em>
				<p>{{ post.content }}</p>
			</article>
	{% endfor %}
	</section>
{% endblock %}
```
Salve todas as alterações e então acesse [http://localhost:8000/blog/](http://localhost:8000/blog/) e as postagens serão exibidas:

![](https://github.com/guicarvalho/django-os-primeiros-passos/blob/master/imagens/dj-blog-home.png)

## Exibindo a postagem
É comum na página inicial serem exibidos textos mais curtos, onde é passada uma breve descrição do assunto da postagem. Na grande maioria dos blogs, o usuário pode clicar no título do *post* para ver todo o conteúdo da publicação. Vamos implementar esse comportamento no nosso blog também.

Abra o arquivo `blog/routes.py` e adicione uma nova URL:
```python
url(r'(?P<post_slug>[-\w]+)/$', views.detail, name='post-detail'),
```
Agora precisamos criar a função `detail`, abra o arquivo `blog/views.py` e adicione a função:
```python
from django.shortcuts import get_object_or_404, render

from blog.models import Post


def index(request):
    last_posts = Post.objects.all().order_by('-created_at')[:5]

    ctx = {'last_posts': last_posts}

    return render(request, 'blog/index.html', ctx)


def detail(request, post_slug):
    post = get_object_or_404(Post, post_slug=post_slug)

    ctx = {'post': post}

    return render(request, 'blog/detail.html', ctx)
```
Agora precisamos criar o *template* para exibir o conteúdo da publicação, crie o arquivo `blog/templates/blog/detail.html`:
```html
{% extends 'base.html' %}

{% block title %} {{ post.title }} {% endblock %}

{% block content %}
<section id="post">
	<article>
		<h1>{{ post.title }}</h1>
		<em>{{ post.created_at }}</em>
		<p>{{ post.content }}</p>
	</article>
</section>
{% endblock %}
```
Se você tentar acessar a página [http://localhost:8000/blog/python/](http://localhost:8000/blog/python/), irá receber um erro informando que o campo *post_slug* não existe. Precisamos criá-lo, vamos alterar o modelo `Post` e adicionar o novo campo.
```python
# blog/models.py

from django.db import models


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    post_slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
```
Agora vamos gerar o script de migração e aplicá-lo para evoluir nosso banco de dados.
```sh
~$ ./manage.py makemigrations
You are trying to add a non-nullable field 'post_slug' to post without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
Select an option: 1
Please enter the default value now, as valid Python
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
Type 'exit' to exit this prompt
>>> slug
Migrations for 'blog':
  blog/migrations/0002_post_post_slug.py
    - Add field post_slug to post

~$ ./manage.py migrate
```
Quando executamos a migração um erro ocorre, isso acontece pois configuramos o campo para ser UNIQUE e nosso script sempre atribui o valor `slug_` para os campos que não tem slug preenchida.

Para solucionar esse problema podemos adicionar a *flag* `null=True` na migração gerada, executar a migração e depois remover a *flag*.
```python
# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 02:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_slug',
            field=models.SlugField(unique=True, null=True),
        ),
    ]
```
Depois de executar lembre-se de voltar a versão original:
```python
# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 02:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_slug',
            field=models.SlugField(default='slug', unique=True),
            preserve_default=False,
        ),
    ]
```
Seria bom que a *slug* fosse gerada automaticamente no momento em que a postagem é salva. A boa notícia é que o Django Admin pode nos ajudar com isso, edite o arquivo `blog/admin.py` e adicione o campo `prepopulated_fields`:
```python
from django.contrib import admin

from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at',)
    search_fields = ('title',)
    prepopulated_fields = {'post_slug': ('title',)}


admin.site.register(Post, PostAdmin)
```
Vamos até o Django Admin e editar as nossas postagens para que a slug seja gerada em cada uma delas. Edite as postagens, quando você clicar no campo de título, automaticamente o Django irá gerar a slug:

![](https://github.com/guicarvalho/django-os-primeiros-passos/blob/master/imagens/dj-admin-slug-edit.png) 

Agora conseguimos acessar [http://localhost:8000/blog/django-os-primeiros-passos/](http://localhost:8000/blog/django-os-primeiros-passos/).

![](https://github.com/guicarvalho/django-os-primeiros-passos/blob/master/imagens/dj-post-detail.png)

O último passo que temos que fazer é transformar os títulos em link, para quando clicarmos nele ser redirecionados para a página da postagem. Abra o *template* `blog/templates/blog/index.html`:
```html
{% extends 'base.html' %}

{% block title %} Últimas postagens {% endblock %}

{% block content %}
	<section id="last-posts">
		<header>
			<h1>Últimas postagens</h1>
		</header>
	{% for post in last_posts %}
			<article>
				<h1><a href="{% url 'post-detail' post.post_slug %}">{{ post.title }}</a></h1>
				<em>{{ post.created_at }}</em>
				<p>{{ post.content }}</p>
			</article>
	{% endfor %}
	</section>
{% endblock %}
```
![](https://github.com/guicarvalho/django-os-primeiros-passos/blob/master/imagens/dj-index-links.png) 

### Refatorando os testes do modelo
Vamos escrever um teste para garantir que a slug não se repita. Adicione o método ao arquivo `blog/tests/test_models.py`
```python
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
```
Estamos executando nosso teste dentro de uma transação, quando fazemos isso nossa classe de teste deve extender de `TransactionTestCase`. Faça essa alteração também, e não se esqueça do  *import*. Ao final seu arquivo deve estar assim:
```python
from django.db.utils import IntegrityError

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
```
Execute os testes `./manage.py test -v 1`.
```sh
....
----------------------------------------------------------------------
Ran 4 tests in 0.075s

OK
```