# 05 - Adicionando estilo
Vamos adicionar um pouco de estilo CSS em nossas páginas, vamos fazer o uso do [Bulma.io](https://bulma.io/).

Primeiramente vamos dizer ao Django como ele faz para servir nossos arquivos estáticos e também onde eles podem ser encontrados, para isso temos que alterar o `settings.py`.
```python
# settings.py

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/var/www/blogguinho/static/')
STATICFILES_DIRS = ['static']
```
No diretório raíz do projeto crie uma pasta com o nome `static`, nessa pasta vamos colocar nossos arquivos *CSS e JS*. Agora dentro dessa pasta crie uma nova pasta com o nome de *css*. Vamos baixar o código do *bulma* e salvar o arquivo dentro da pasta *CSS*.
```sh
├── static
│   └── css
│       └── bulma.min.css
```
Precisamos configurar uma rota para arquivos estáticos, essa rota será usada para o Django servir os arquivos. Sem ela, ao abrir a página o HTML vai "pedir" o arquivo e o servidor (Django) irá responder 404 (Not Found), pois ele não sabe como encontrar o conteúdo. Abra o arquivo `blogguinho/routes.py` e então deixe-o como a seguir:
```python
from django.contrib import admin

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

```
Vamos alterar o `base.html` incluindo o bulma em nosso projeto.
```html
{% load static %}

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Blogguinho - {% block title %}{% endblock %}</title>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" integrity="sha256-eZrrJcwDc/3uDhsdt61sL2oOBY362qM3lon1gyExkL0=" crossorigin="anonymous" />
  <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
	<link rel="stylesheet" href="{% static 'css/bulma.min.css' %}">
	<link rel="stylesheet" href="{% static 'css/blog.css' %}">
</head>
<body>
	<div class="container">
		<!-- START NAV -->
    <nav class="navbar is-white">
      <div class="navbar-brand">
        <a class="navbar-item brand-text" href="../">
          Blogguinho        
        </a>
        <div class="navbar-burger burger" data-target="navMenu">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
      <div id="navMenu" class="navbar-menu">
        <div class="navbar-start">
          <a class="navbar-item" href="#">
            Home
          </a>
          <a class="navbar-item" href="#">
            Postagens
          </a>
        </div>
      </div>
    </nav>
    <!-- END NAV -->
		{% block content %}
		{% endblock %}
	</div>
</body>
</html>
```
Além do bulma, incluimos também *font-awesome*, a font *Open Sans* e um arquivo *css* chamado `blog.css`. Vamos criar o arquivo `static/css/blog.css`:
```css
html,body {
  font-family: 'Open Sans', sans-serif;
  font-size: 14px;
  background: #F0F2F4;
}
.navbar.is-white {
  background: #F0F2F4;
}
.navbar-brand .brand-text {
  font-size: 1.11rem;
  font-weight: bold;
}
.articles {
  margin: 5rem 0;
}
.articles .content p {
    line-height: 1.9;
    margin: 15px 0;
}
.author-image {
    position: absolute;
    top: -30px;
    left: 50%;
    width: 60px;
    height: 60px;
    margin-left: -30px;
    border: 3px solid #ccc;
    border-radius: 50%;
}
.media-center {
  display: block;
  margin-bottom: 1rem;
}
.media-content {
  margin-top: 3rem;
}
.article, .promo-block {
  margin-top: 6rem;
}
div.column.is-8:first-child {
  padding-top: 0;
  margin-top: 0;
}
.article-title {
  font-size: 2rem;
  font-weight: lighter;
  line-height: 2;
}
.article-subtitle {
  color: #909AA0;
  margin-bottom: 3rem;
}
.article-body {
  line-height: 1.4;
  margin: 0 6rem;
}
.promo-block .container {
  margin: 1rem 5rem;
}
```
