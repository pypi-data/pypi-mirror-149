import re
from clld.web.util.helpers import link
from clld.web.util.htmllib import HTML
from clld.web.util.htmllib import literal


GLOSS_ABBR_PATTERN = re.compile(
    "(?P<personprefix>1|2|3)?(?P<abbr>[A-Z]+)(?P<personsuffix>1|2|3)?(?=([^a-z]|$))"
)


def rendered_gloss_units(request, sentence):
    units = []
    if sentence.analyzed and sentence.gloss:
        slices = {sl.index: sl for sl in sentence.forms}
        for pwc, (pword, pgloss) in enumerate(
            zip(sentence.analyzed.split("\t"), sentence.gloss.split("\t"))
        ):
            for gwc, (word, gloss) in enumerate(
                zip(pword.split("="), pgloss.split("="))
            ):
                i = pwc + gwc
                if i not in slices:
                    units.append(
                        HTML.div(
                            HTML.div(word),
                            HTML.div(word, class_="morpheme"),
                            HTML.div(gloss, **{"class": "gloss"}),
                            class_="gloss-unit",
                        )
                    )
                else:
                    units.append(
                        HTML.div(
                            HTML.div(
                                rendered_form(request, slices[i].form, structure=False)
                            ),
                            HTML.div(
                                rendered_form(request, slices[i].form),
                                class_="morpheme",
                            ),
                            HTML.div(gloss, **{"class": "gloss"}),
                            class_="gloss-unit",
                        )
                    )
    return units


def rendered_form(request, ctx, structure=True):
    if structure:
        if ctx.morphs != []:
            return literal(
                "-".join(
                    [
                        link(request, form.morph, label=form.morph.name.strip("-"))
                        for form in ctx.morphs
                    ]
                )
            )
        return literal("&nbsp;")
    return link(request, ctx)