#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from AI2 import create_app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
