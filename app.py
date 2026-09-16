import os
import logging
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///policy_simulator.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Add custom Jinja2 filter for JSON serialization
@app.template_filter('tojsonfilter')
def to_json_filter(obj):
    """Convert object to JSON for JavaScript"""
    try:
        # Convert objects with to_dict method
        if hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):
            json_list = []
            for item in obj:
                if hasattr(item, 'to_dict'):
                    json_list.append(item.to_dict())
                else:
                    json_list.append(str(item))
            return json.dumps(json_list)
        elif hasattr(obj, 'to_dict'):
            return json.dumps(obj.to_dict())
        else:
            return json.dumps(obj)
    except Exception:
        return json.dumps([])

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()
    
    # Import and register routes
    from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
