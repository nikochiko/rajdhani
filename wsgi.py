"""
'app' in this module is a WSGI app.

This is the convention used by boring-serverless to
locate the entrypoint for an application.
"""

# redirect the prints to stderr to avoid interfering with CGI
# See https://github.com/pipalacademy/rajdhani/issues/14
import sys
sys.stdout = sys.stderr

from rajdhani.app import app
