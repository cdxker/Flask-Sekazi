# Flask Sekazi

A jinja extension that adds the features of
django-sekazi into flask

With Flask-Sekazi you can define placeholders where your blocks get rendered and at different places in your templates append to those blocks. This is especially useful for css and Javascript. Our sub-templates can now define css and Javascript files to be included, and the css will be nicely put at the top and the Javascript to the bottom, just like you should. Also sekazai will ignore any duplicate content in a single block.

## Installation

Installation Flask-Sekazi with pip
```
pip install Flask-Sekazi
```

## Usage

To use the extension simply import the class wrapper and pass the Flask app object back to here. Do so like this:
```
from flask import flask
from flask_sekazi import Sekazi

app = Flask(__name__)
sekazi = Sekazi(app)
```
or

Alternativly you can initialize it using `init_app`
```
app = Flask
sekazi = Sekazi()
sekazi.init_app(app)
```

## Example 

Sekazi uses `renderblock` and `addtoblock` to handle unique code snippets define your blocks using `{% renderblock <name> %} and add data to your block using `{% addtoblock <name> %}` 
Example template:
```html
<html>
<head>
{% renderblock "css" %}
</head>
<body>
Your content comes here.
Maybe you want to throw in some css:


{% addtoblock "css" %}
    <link href="/media/css/stylesheet.css" media="screen" rel="[stylesheet](stylesheet)" type="text/css" />
{% endaddtoblock %}


Some more content here.


{% addtoblock "js" %}
    <script type="text/javascript">
        alert("Hello flask");
    </script>
{% endaddtoblock %}


And even more content.
{% renderblock "js" %}
</body>
</html>
```
Above example will render roughly to 
```html
<html>
<head>
<link href="/media/css/stylesheet.css" media="screen" rel="stylesheet" type="text/css" />
</head>
<body>
Your content comes here.
Maybe you want to throw in some css:
Some more content here.
And even more content.
<script type="text/javascript">
alert("Hello flask");
</script>
</body>
</html>
```

It is recommended to have all `renderblock` tags in your base template, the one that gets extended by all other templates

## Sekazi Data is unique

All data in sekizai is enforced to be unique within its block namespace. This is because the main purpose of sekizai is to handle javascript and css dependencies in templates.

A simple example of this action will be this template
```html


{% addtoblock "js" %}
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/mootools/1.3.0/mootools-yui-compressed.js"></script>
{% endaddtoblock %}

{% addtoblock "js" %}
    <script type="text/javascript">
        $('firstelement').set('class', 'active');
    </script>
{% endaddtoblock %}

{% addtoblock "js" %}
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/mootools/1.3.0/mootools-yui-compressed.js"></script>
{% endaddtoblock %}

{% addtoblock "js" %}
    <script type="text/javascript">
        $('secondelement').set('class', 'active');
    </script>
{% endaddtoblock %}

{% renderblock "js" %}
```
Which renders down to
```html
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/mootools/1.3.0/mootools-yui-compressed.js"></script>
<script type="text/javascript">
    $('firstelement').set('class', 'active');
</script>
<script type="text/javascript">
    $('secondelement').set('class', 'active');
</script>
```

An example of using this in a flask application is found under the `examples` folder

