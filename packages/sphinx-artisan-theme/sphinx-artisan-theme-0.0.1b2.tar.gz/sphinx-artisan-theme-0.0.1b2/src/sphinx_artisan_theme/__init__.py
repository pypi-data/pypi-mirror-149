"""
A sphinx theme for Artisan of Code projects.
"""

import docutils.nodes
import pkg_resources
import pathlib
import typing

import markupsafe
import sphinx.application
import sphinx.config
import sphinx.util.fileutil

__version__ = pkg_resources.get_distribution(__name__).version

THEMES_ROOT = pathlib.Path(__file__).parent.absolute() / "themes"

HTML_PERMALINK_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" class="inline align-text-middle" style="height: 0.7em" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
  <path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
</svg>
"""


def _config_inited(
    app: sphinx.application.Sphinx,  # pylint: disable=unused-argument
    config: sphinx.config.Config,  # pylint: disable=unused-argument
) -> None:
    """
    config-inited callback

    Update our config here.

    :param app: the sphinx application
    :param config: the sphinx config
    """


def _builder_inited(app: sphinx.application.Sphinx):
    if app.builder.format == "html":
        app.add_css_file("https://rsms.me/inter/inter.css")
        app.add_css_file("theme.css")


def _html_page_context(
    app: sphinx.application.Sphinx,
    pagename: str,  # pylint: disable=unused-argument
    templatename: str,  # pylint: disable=unused-argument
    context: dict[str, object],
    doctree: docutils.nodes.document | None,  # pylint: disable=unused-argument
) -> None:
    context["html_permalinks_icon"] = markupsafe.Markup(app.config.html_permalinks_icon)

    context["root_title"] = app.env.titles[context["root_doc"]].astext()

    if pagename in app.env.titles:
        context["pagetitle"] = app.env.titles[pagename].astext()

    if app.config.author != "unknown":
        context["author"] = app.config.author

    if app.config.author_url != "unknown":
        context["author_url"] = app.config.author_url


def setup(app: sphinx.application.Sphinx) -> dict[str, typing.Any]:
    """
    Registration callback

    Setup the extension with sphinx

    :param app: the sphinx application
    """

    for path in THEMES_ROOT.iterdir():
        if not path.joinpath("theme.conf").exists():
            continue

        app.add_html_theme(path.name, path)

    app.setup_extension("sphinx_artisan_theme.ext.extract_toc")
    app.setup_extension("sphinx_artisan_theme.ext.remove_sections")

    app.connect("builder-inited", _builder_inited)
    app.connect("config-inited", _config_inited)
    app.connect("html-page-context", _html_page_context)

    app.add_config_value("author_url", default="unknown", rebuild="html", types=[str])

    app.config.html_permalinks_icon = HTML_PERMALINK_ICON

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
