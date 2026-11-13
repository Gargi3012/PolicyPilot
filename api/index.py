import os
import sys

# Add project root directory to sys.path so imports work in Vercel serverless environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class VercelPathMiddleware:
    """
    WSGI middleware to normalize PATH_INFO for Vercel serverless functions.
    Vercel rewrites to /api/index or /api/index.py, which leaves an unwanted
    prefix in PATH_INFO that causes Flask to return 404.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "")
        matched_path = environ.get("HTTP_X_MATCHED_PATH") or environ.get("HTTP_X_FORWARDED_URI")
        
        if matched_path and not matched_path.startswith("/api/index"):
            environ["PATH_INFO"] = matched_path
        else:
            for prefix in ["/api/index.py", "/api/index", "/api"]:
                if path.startswith(prefix):
                    new_path = path[len(prefix):]
                    environ["PATH_INFO"] = new_path if new_path.startswith("/") else ("/" + new_path if new_path else "/")
                    break

        return self.wsgi_app(environ, start_response)

# Wrap Flask WSGI application with the Vercel path normalizer
app.wsgi_app = VercelPathMiddleware(app.wsgi_app)
