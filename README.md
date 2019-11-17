# Flask Sekazi

A jinja extension that adds the features of
django-sekazi into flask

With Flask-Sekazi you can define placeholders where your blocks get rendered and at different places in your templates append to those blocks. This is especially useful for css and Javascript. Our sub-templates can now define css and Javascript files to be included, and the css will be nicely put at the top and the Javascript to the bottom, just like you should. Also sekazai will ignore any duplicate content in a single block.

## Installation
Installation can be done using pip or pipenv with
```
pipenv install Flask-Sekazi
```

## Usage

You can simply add it the top of the file as such
```
from flask import flask
from flask_sekazi import Sekazi

app = Flask(__name__)
sekazi = Sekazi(app)
```
or

Initalize it using the `init_app` function

```
app = Flask
sekazi = Sekazi()
sekazi.init_app(app)
```

