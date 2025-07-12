"""
Custom routing helpers to avoid werkzeug BuildError exceptions
"""

from flask import current_app, request

def safe_url_for(endpoint, **values):
    """
    Safe version of url_for that won't raise BuildError
    Returns # if the endpoint doesn't exist
    """
    try:
        from flask import url_for
        return url_for(endpoint, **values)
    except Exception as e:
        # Log the error for debugging
        if current_app:
            current_app.logger.warning(f"Route build error for {endpoint}: {e}")
        return "#"

def route_exists(endpoint):
    """
    Check if a route endpoint exists
    """
    try:
        from flask import url_for
        url_for(endpoint)
        return True
    except:
        return False
