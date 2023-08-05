"""Top-level package for clld-corpus-plugin."""
from clld_corpus_plugin import interfaces
from clld_corpus_plugin import models


__author__ = "Florian Matter"
__email__ = "florianmatter@gmail.com"
__version__ = "0.0.1"


def includeme(config):
    config.registry.settings["mako.directories"].insert(
        1, "clld_corpus_plugin:templates"
    )
    config.register_resource("text", models.Text, interfaces.IText, with_index=True)
    config.register_resource(
        "wordform", models.Wordform, interfaces.IWordform, with_index=True
    )
