from clld_morphology_plugin import interfaces
from clld_morphology_plugin import models


__author__ = "Florian Matter"
__email__ = "florianmatter@gmail.com"
__version__ = "0.0.1"


def includeme(config):
    config.registry.settings["mako.directories"].insert(
        1, "clld_morphology_plugin:templates"
    )
    config.register_resource("morph", models.Morph, interfaces.IMorph, with_index=True)
    config.register_resource(
        "morpheme",
        models.Morpheme,
        interfaces.IMorphset,
        with_index=True,
        with_detail=True,
    )
    config.register_resource(
        "meaning", models.Meaning, interfaces.IMeaning, with_index=True
    )
    config.register_resource(
        "wordform", models.Wordform, interfaces.IWordform, with_index=True
    )
