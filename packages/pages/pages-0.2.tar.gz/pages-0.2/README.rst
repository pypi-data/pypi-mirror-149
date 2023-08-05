Pages
=====

Pages is a simple command line static site generator.

Piglet, Jinja2, Chameleon, Genshi and Kajiki templating systems are all
supported, and content can be read from reStructuredText, markdown or JSON data
files.

Quick start
-----------


::

    pip install pages

    pages --template layout.html --output build/ src/*


Extra data can be made available to the rendered template, by loading
data from python code or JSON::

    # Inline JSON
    pages --template layout.html --context '{"foo": "bar"}' src/*

    # a JSON file
    pages --template layout.html --context data.json  src/*

    # JSON loaded from a remote API
    pages --template layout.html --context <(curl -s 'wttr.in/?format=j1') src/*

    # A python module
    pages --template layout.html --context myproject.somemodule:avariable src/*

    # A python script
    pages --template layout.html --context somevars.py src/*
