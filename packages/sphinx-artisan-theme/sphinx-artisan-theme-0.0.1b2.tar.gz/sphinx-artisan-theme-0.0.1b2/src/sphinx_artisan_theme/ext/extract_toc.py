"""
Provides jinja2 helpers for customisable tables of contents.
"""

from __future__ import annotations

import dataclasses
import docutils.nodes
import typing


import sphinx.addnodes
import sphinx.application
import sphinx.environment.adapters.toctree


@dataclasses.dataclass
class NavigationItem:
    """
    Navigation item

    Represents an individual link in a table of contents.

    :param title: visible title
    :param url: link address
    :param children: child navigation items
    :param is_active: is the current active page
    """

    title: str
    url: str
    children: list[NavigationItem]
    is_active: bool


@dataclasses.dataclass
class NavigationSection:
    """
    Navigation section

    represents a section of the table of contents with optional title.

    :param title: visible title
    :param children: child navigation items
    """

    title: str | None
    children: list[NavigationItem]


def _node_to_navigation_items(node: docutils.nodes.bullet_list) -> list[NavigationItem]:
    """
    Node to NavigationItem

    convert a docutils TocTree recursively into a tree of :class:`NavigationItem`.

    :param node: a bulleted list of references from docutils

    :returns: a generic non docutils representation
    """

    items = []

    for child in node.children:
        reference = child.next_node(docutils.nodes.reference)

        if not reference:
            continue

        bullet_list = child.next_node(docutils.nodes.bullet_list)

        item = NavigationItem(
            title=reference.astext(),
            url=reference["refuri"],
            children=(_node_to_navigation_items(bullet_list) if bullet_list else []),
            is_active="current" in child["classes"],
        )

        items.append(item)

    return items


def _html_page_context(
    app: sphinx.application.Sphinx,
    pagename: str,
    templatename: str,  # pylint: disable=unused-argument
    context: dict[str, object],
    doctree: docutils.nodes.document | None,  # pylint: disable=unused-argument
) -> None:
    """
    html-page-context callback

    Wire up our custom jinja2 helpers.

    :param app: the sphinx application
    :param pagename: the canonical name of the page being rendered
    :param templatename: the name of the template to render
    :param context: the jinja2 context
    :param doctree: reST doctree
    """

    def get_navigation(**kwargs: object) -> list[NavigationItem]:
        """
        Get navigation

        :returns: the navigation tree
        """

        builder = sphinx.environment.adapters.toctree.TocTree(app.env)

        kwargs.setdefault("collapse", False)

        toctree = builder.get_toctree_for(pagename, app.builder, **kwargs)

        sections = []

        title = None

        if not toctree:
            return []

        for child in toctree.children:

            if isinstance(child, docutils.nodes.title):
                title = child.astext()

            if isinstance(child, docutils.nodes.bullet_list):
                section = NavigationSection(
                    title=title,
                    children=_node_to_navigation_items(child),
                )
                sections.append(section)

                title = None

        return sections

    def get_table_of_contents() -> list[NavigationItem]:
        """
        Get page navigation

        :returns: the pages navigation tree
        """

        builder = sphinx.environment.adapters.toctree.TocTree(app.env)

        toctree = builder.get_toc_for(pagename, app.builder)

        if not toctree:
            return []

        root = _node_to_navigation_items(toctree)

        return root[0].children if root else []

    context["get_navigation"] = get_navigation
    context["get_table_of_contents"] = get_table_of_contents


def setup(app: sphinx.application.Sphinx) -> dict[str, typing.Any]:
    """
    Registration callback

    Setup the extension with sphinx

    :param app: the sphinx application
    """

    app.connect("html-page-context", _html_page_context)

    return {"parallel_read_safe": True, "parallel_write_safe": True}
