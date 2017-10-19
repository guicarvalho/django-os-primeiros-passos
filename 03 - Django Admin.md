# 03 - Django Admin
Django por ser um framework fullstack carrega com sigo soluções embutidas para problemas comuns enfrentados durante o desenvolvimento de sistemas web.

Django Admin é uma das principais *features* que o Django tem embutida e com certeza poupará grande parte de seus esforços em 90% dos sistemas que terá que desenvolver. 

Para acessar a interface administrativa, rode o servidor de desenvolvimento e acesse `http://localhost:8000/admin`. Você será redirecionado para a tela de login, mas ainda não criamos um usuário com acesso.

Abra uma nova aba no terminal para criarmos o usuário:
```shell
~$ ./manage.py createsuperuser
Username (leave blank to use 'guilherme'): admin
Email address: admin@admin.com
Password: 
Password (again):
Superuser created successfully.
```
Agora podemos voltar a tela de login e preencher o formulário com as informações do usuário recém criado. Depois de efetuar o login, a tela home do admin será exibida:

![](/home/guilherme/Documentos/Projetos/TempoRealEventos/django-os-primeiros-passos/imagens/dj-admin-home.png) 

Excelente! Podemos editar Grupos e Usuários, mas ainda não conseguimos manipular as postagens. Isso ocorre pois o Django espera que você informe quais *modelos* devem ser exibidos na interface administrativa.

Vamos registrar o modelo de `Post` para que possamos cadastrar novas postagens. Abra o arquivo `blog/admin.py`, e edite conforme a seguir:
```python
from django.contrib import admin
from blog.models import Post

admin.site.register(Post)
```
Recarregue a página da área administrativa, agora foi adicionado um novo link onde podemos gerenciar as postagens.

![](/home/guilherme/Documentos/Projetos/TempoRealEventos/django-os-primeiros-passos/imagens/dj-admin-post-menu.png)

Agora podemos fazer alguns testes, criando, editando e excluindo postagens.

## Customizando a interface do Admin
Nos podemos customizar a forma como os dados são exibidos, filtrados e organizados na interface do admin. Para isso basta editar o arquivo `blog/admin.py`.

Vamos alterar a listagem das postagens para que exiba o título, data de criação e um campo de filtro para filtrar por título:
```python
from django.contrib import admin

from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at',)
    search_fields = ('title',)


admin.site.register(Post, PostAdmin)
```
Você deve ter algo parecido com:

![](/home/guilherme/Documentos/Projetos/TempoRealEventos/django-os-primeiros-passos/imagens/dj-admin-custom-post-list.png) 

Existem muitas outras possibilidades que podem serem usadas na área administrativa, para mais detalhes acesso a documentação oficial [The Django admin site](https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#modeladmin-objects).