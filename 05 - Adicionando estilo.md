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
Vamos alterar o `base.html` incluindo o bulma em nosso projeto.
```html

```