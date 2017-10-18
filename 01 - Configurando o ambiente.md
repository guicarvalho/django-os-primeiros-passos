# 01 - Configurando o ambiente
A primeira coisa que precisamos fazer para iniciar o nosso projeto é configurar o nosso ambiente de desenvolvimento.

* Mint 17.2 (Pode usar Ubuntu)
*  Sublime Text 3
* Python 3.6

## Pyenv
O uso do Pyenv é opcional, ele apenas facilita o gerenciamento das versões de Python em seu Sistema Operacional. Para instalar é bem simples:
```shell
~$ curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash

# Edite o arquivo ~/.bashrc e coloque as linhas a seguir no final do arquivo
export PATH="/home/guilherme/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# instale a versão 3.6
~$ pyenv install 3.6.3
```

## Criando o projeto
Vamos criar a estrutura inicial do nosso projeto, primeiramente vamos criar uma pasta para o curso, vou chamar de **Curso Django**. Depois vamos instalar o Django e iniciar o nosso servidor para ver se tudo está correndo bem.

```sh
~$ mkdir Curso\ Django
~$ cd Curso\ Django
~$ pyenv local 3.6.3  # apenas para quem está utilizando o pyenv
~$ python -m venv .blogguinho
~$ pip install django

# criando a estrtura de pastas do projeto
~$ django-admin startproject blogguinho
~$ cd blogguinho
~$ tree
.
├── blogguinho
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py

~$ ./manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).

You have 13 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.

October 18, 2017 - 02:09:36
Django version 1.11.6, using settings 'blogguinho.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
Abra o browser e acesse `http://localhost:8000`, se tudo deu certo você deve ver uma tela parecida com essa:
![](https://github.com/guicarvalho/django-os-primeiros-passos/blob/master/imagens/dj-localhost-first-time.png) 
