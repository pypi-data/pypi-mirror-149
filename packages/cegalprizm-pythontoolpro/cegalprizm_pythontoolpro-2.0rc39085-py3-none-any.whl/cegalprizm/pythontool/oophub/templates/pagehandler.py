# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.




import pkg_resources
from cegalprizm.pythontool.grpc._logo import _logo_data_uri

from pathlib import Path
import os

def _get_version():
    return pkg_resources.get_distribution('cegalprizm-pythontoolpro').version

def get_template(fn):
    root = Path(__file__).parent
    with open(os.path.join(root, fn), "r") as f:
        return f.read()

class FormatDict(dict):
    def __missing__(self, key):
        return "{" + str(key)+"}"

class PtpPageHandler:
    _content = {
        "logo":_logo_data_uri,
        "user_version": _get_version()}

    def landing_page(self):
        """Returns the HTML that the user sees after authenticating, briefly, and redirects to the /landing page.  Instructs the server to continue serving further requests"""
        return (
            True,
            get_template('authenticating.html').format_map(FormatDict(self._content))
        )

    def get(self, parsed_url, access_token_factory):
        """A minimal example of routing and serving the /landing page
        
        Note:  a full-fledged http and routing abstraction is overkill for our current use-cases, but 
        it could easily evolve from this."""
        
        if parsed_url.path == "/landing":
            return (False, get_template('landing.html').format_map(FormatDict(self._content)))
        else:
            # continue serving if another page (e.g. at least /favicon.ico!) is requested
            return (True, "")