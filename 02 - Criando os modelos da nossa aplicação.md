# 02 - Criando os modelos da nossa aplicação
Os modelos são classes Python que representam as tabelas no banco de dados. Esse mecanismo é conhecido como ORM (Object Relational Model), por padrão o Django já tem um ORM embutido para que possamos manipular os nossos registros através de objetos.

O Django suporta os mais populares banco de dados, e por isso precisamos dizer para ele qual o banco de dados que nossa aplicação vai utilizar. No nosso caso vamos utilizar o **Sqlite**, que é um banco simples e muito usado em ambiente de desenvolvimento.

Para fazer a configuração do banco de dados precisamos editar o arquivo `settings.py`. Dentro do arquivo de configuração temos um dicionário com o nome **DATABASES**. Por padrão o Django já vem com o **Sqlite** configurado, temos apenas que informar qual será o nome da nossa base de dados.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'blogguinho.db'),
    }
}
```
Outro recurso que precisamos constantemente no desenvolvimento de sistemas web é migração de banco de dados, que consiste em atualizar a estrutura do banco de dados versionando essas modificações. Assim como o ORM o Django possue uma ferramenta embutida para tratar migração de banco de dados.

Vamos rodar essa ferramenta para que a primeira versão do banco seja gerada.
```sh
~$ ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying sessions.0001_initial... OK
```
Agora podemos conferir se foi criado o arquivo `blogguinho.db` na pasta do projeto.
```sh
~$ ls
blogguinho  blogguinho.db  manage.py
```
O comando **migrate** cria as tabelas baseado nos apps que estão instalados na lista **INSTALLED_APPS** no arquivo `settings.py`.

## Criando a nossa app
Em Django temos o conceito de APP, que são módulos plugáveis em projetos. Sempre pense em seu projeto como um conjunto de APP's. Isso facilita reutilizar código, uma vez que sua APP pode ser aproveitada em outros projetos.

Para criar uma nova APP:
```sh
~$ ./manage.py startapp blog
blog  blogguinho  blogguinho.db  manage.py
``` 
Como dissemos anteriormente o Django possui um ORM, então para criar uma tabela no nosso banco de dados devemos criar uma classe Python. As classes devem estar definidas em `<myapp>/models.py`.
```python
from django.db import models


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
```
A classe `Post` herda de `models.Model`, dessa forma ela define a tabela no banco de dados assim como seus campos: `created_at, title e content`. Essa classe irá representar as postagens que são feitas em nosso blog.

Por padrão o Django cria um campo único com o nome de `id` para todas as tabelas. Ou seja, toda vez que um novo Post é cadastrado o Django automaticamente se encarrega de preencher o campo `id`.

O campo `created_at` possui o atributo `auto_now_add=True`, isso indica que quando o registro for criado a data do momento de criação será atribuida para esse campo.

Dessa forma para adicionarmos um novo `Post` precisamos apenas informa `title e content`.

## Atualizando o banco de dados
Adicionamos uma nova classe de mapeamento em nosso projeto, então precisaremos gerar o script de migração para que o Django possa atualizar o banco de dados.

Se rodarmos o comando `./manage.py makemigrate` o Django irá informar que não existem migrações para serem aplicadas, porém, sabemos que isso não é verdade.

Isso acontece pois o Django não tem conhecimento que nossa aplicação `blog` existe, então precisamos informar ao Django que temos uma nova APP em nosso projeto. Para isso precisamos instalar a APP no projeto, podemos fazer isso alterando o dicionário **INSTALLED_APPS**.
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Local apps
    'blog',
]
```
Agora se rodarmos o comando para gerar as migrações novamente teremos um novo resultado.
```shell
~$ ./manage.py makemigrations
Migrations for 'blog':
  blog/migrations/0001_initial.py
    - Create model Post
```
O comando `makemigrations` diz ao Django que mudanças foram feitas nos modelos e nos queremos criar a migração. As migrações ficam armazenas em `<appname>/migrations/`. Aqui está a migrations que foi gerada para criar a tabela Post.
```python
# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-18 03:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
            ],
        ),
    ]
```
Para que as tabelas sejam criadas, preciamos aplicar a migração.
```shell
~$ ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions
Running migrations:
  Applying blog.0001_initial... OK
```
Importante lembrar que para atualizar o banco de dados devemos:

* Alterar o arquivo `model.py`
* Gerar as migrações com o comando `makemigrations`
* Aplicar os scripts de migração com o comando `migrate`

## Conhecendo a API do ORM
Django fornece um terminal Python interativo para acessar  a Django API. Para iniciar o Shell.
```shell
~$ ./manage.py shell
```
