"""
Remove section tags from sphinx html output.
"""

import docutils.nodes
import docutils.writers._html_base
import typing

import sphinx.application


def _visit_section_html(
    translator: docutils.writers._html_base.HTMLTranslator,
    node: docutils.nodes.section,  # pylint: disable=unused-argument
) -> None:
    translator.section_level += 1


def _depart_section_html(
    translator: docutils.writers._html_base.HTMLTranslator,
    node: docutils.nodes.section,  # pylint: disable=unused-argument
) -> None:
    translator.section_level -= 1


def _visit_title_html(
    translator: docutils.writers._html_base.HTMLTranslator,
    node: docutils.nodes.section,
) -> None:
    if isinstance(node.parent, docutils.nodes.section):
        ids = node.get("ids")

        node["ids"] = node.parent["ids"]

        translator.__class__.visit_title(translator, node)

        if ids:
            node["ids"] = ids
        else:
            del node["ids"]

        return

    translator.__class__.visit_title(translator, node)


def _depart_title_html(
    translator: docutils.writers._html_base.HTMLTranslator,
    node: docutils.nodes.section,  # pylint: disable=unused-argument
) -> None:
    translator.__class__.depart_title(translator, node)


def setup(app: sphinx.application.Sphinx) -> dict[str, typing.Any]:
    """
    Registration callback

    Setup the extension with sphinx

    :param app: the sphinx application
    """

    app.add_node(
        docutils.nodes.section,
        override=True,
        html=(_visit_section_html, _depart_section_html),
    )

    app.add_node(
        docutils.nodes.title,
        override=True,
        html=(_visit_title_html, _depart_title_html),
    )

    return {"parallel_read_safe": True, "parallel_write_safe": True}
