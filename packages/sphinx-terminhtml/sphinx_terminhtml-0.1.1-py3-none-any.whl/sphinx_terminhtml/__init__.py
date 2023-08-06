"""
Write bash commands in a Sphinx directive, output an animated HTML/CSS terminal
"""
from sphinx_terminhtml.sphinx_setup import setup
from sphinx_terminhtml.directives import (
    TerminHTMLDirective,
    create_terminhtml_directive_with_setup,
)
