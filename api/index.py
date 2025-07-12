import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app

# Create the Flask app instance
app = create_app()

# This is the main entry point for Vercel
# Vercel will automatically handle the WSGI interface
