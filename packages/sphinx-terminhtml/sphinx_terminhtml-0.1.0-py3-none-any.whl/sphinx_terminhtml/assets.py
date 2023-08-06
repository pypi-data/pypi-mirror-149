import os
import tempfile
from pathlib import Path

import requests
from sphinx.application import Sphinx
from sphinx.util.fileutil import copy_asset
from terminhtml.main import TerminHTML, CommandResults

js_file_url = "https://unpkg.com/@terminhtml/bootstrap@1.0.0-alpha.9/dist/@terminhtml-bootstrap.umd.js"
js_file_name = "@terminhtml-bootstrap.umd.js"
css_file_name = "ansi2html.css"


def download_and_copy_asset_files(app: Sphinx, exc):
    if exc is not None:
        # Build failed, don't copy assets
        return

    js_content = requests.get(js_file_url).text
    css_content = TerminHTML(command_results=CommandResults(results=[])).styles

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_js_path = Path(tmp_dir) / js_file_name
        tmp_js_path.write_text(js_content)

        tmp_css_path = Path(tmp_dir) / css_file_name
        tmp_css_path.write_text(css_content)

        # Copy asset files
        copy_asset(str(tmp_js_path), os.path.join(app.outdir, "_static"))
        copy_asset(str(tmp_css_path), os.path.join(app.outdir, "_static"))


def register_assets(app: Sphinx):
    app.connect("build-finished", download_and_copy_asset_files)
    app.add_js_file(js_file_name)
    app.add_css_file(css_file_name)
