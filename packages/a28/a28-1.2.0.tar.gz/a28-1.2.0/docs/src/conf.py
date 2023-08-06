"""Configure Sphinx to use pyproject.toml file.

Waiting for https://github.com/sphinx-doc/sphinx/issues/9506 to move all
configuration into pyproject.toml. Until then, use the sphinx_pyproject
module.
"""
from sphinx_pyproject import SphinxConfig

config = SphinxConfig("../../pyproject.toml", globalns=globals())

html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': 'white',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}
