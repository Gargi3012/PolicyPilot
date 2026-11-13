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

class VercelPathMiddleware:
    """Normalize PATH_INFO for Vercel serverless function rewrites."""
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "")
        for prefix in ["/app.py", "/api/index.py", "/api/index", "/api", "/index.py"]:
            if path == prefix:
                environ["PATH_INFO"] = "/"
                break
            elif path.startswith(prefix + "/"):
                environ["PATH_INFO"] = path[len(prefix):]
                break
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(ProxyFix(app.wsgi_app, x_proto=1, x_host=1))

import tempfile

# Configure the database
if os.environ.get("VERCEL"):
    db_file = os.path.join(tempfile.gettempdir(), "policy_simulator.db").replace('\\', '/')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", f"sqlite:///{db_file}")
else:
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
    
    # Auto-seed initial data if database is fresh/empty (e.g. on Vercel deployment)
    try:
        from models import HistoricalPolicy, Policy
        if HistoricalPolicy.query.count() == 0:
            from data_processor import load_historical_data
            load_historical_data()
        
        if Policy.query.count() == 0:
            from data.indian_policy_examples import SAMPLE_INDIAN_POLICIES
            from ml_models import PolicyImpactPredictor
            from models import PolicyPrediction
            predictor = PolicyImpactPredictor()
            for sp in SAMPLE_INDIAN_POLICIES[:6]:
                p = Policy(
                    name=sp['name'],
                    sector=sp['sector'],
                    region=sp['region'],
                    numeric_change=sp['numeric_change'],
                    time_period=sp['time_period'],
                    description=sp.get('description', '')
                )
                db.session.add(p)
                db.session.commit()
                pred = predictor.predict_impact(
                    sector=p.sector,
                    numeric_change=p.numeric_change,
                    time_period=p.time_period,
                    region=p.region
                )
                ppred = PolicyPrediction(
                    policy_id=p.id,
                    gdp_impact=pred['gdp_impact'],
                    inflation_impact=pred['inflation_impact'],
                    unemployment_impact=pred['unemployment_impact'],
                    environmental_impact=pred['environmental_impact'],
                    confidence_score=pred['confidence_score'],
                    sentiment_score=pred.get('sentiment_score', 0),
                    sentiment_confidence=pred.get('sentiment_confidence', 0)
                )
                ppred.set_sector_breakdown(pred['sector_breakdown'])
                db.session.add(ppred)
                db.session.commit()
    except Exception as e:
        logging.warning(f"Initial data seed check: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
