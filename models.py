from app import db
from datetime import datetime
from sqlalchemy import Text, JSON
import json

class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    numeric_change = db.Column(db.Float, nullable=False)
    time_period = db.Column(db.Integer, nullable=False)  # months
    description = db.Column(Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to predictions
    predictions = db.relationship('PolicyPrediction', backref='policy', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sector': self.sector,
            'region': self.region,
            'numeric_change': self.numeric_change,
            'time_period': self.time_period,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class PolicyPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.id'), nullable=False)
    
    # Economic indicators predictions
    gdp_impact = db.Column(db.Float)  # Percentage change
    inflation_impact = db.Column(db.Float)  # Percentage points
    unemployment_impact = db.Column(db.Float)  # Percentage points
    environmental_impact = db.Column(db.Float)  # CO2 emission change %
    
    # Sector-wise breakdown (stored as JSON)
    sector_breakdown = db.Column(Text)  # JSON string
    
    # Confidence scores
    confidence_score = db.Column(db.Float)  # 0-1
    
    # Public sentiment (if applicable)
    sentiment_score = db.Column(db.Float)  # -1 to 1
    sentiment_confidence = db.Column(db.Float)  # 0-1
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_sector_breakdown(self):
        if self.sector_breakdown:
            return json.loads(self.sector_breakdown)
        return {}
    
    def set_sector_breakdown(self, data):
        self.sector_breakdown = json.dumps(data)
    
    def to_dict(self):
        return {
            'id': self.id,
            'policy_id': self.policy_id,
            'gdp_impact': self.gdp_impact,
            'inflation_impact': self.inflation_impact,
            'unemployment_impact': self.unemployment_impact,
            'environmental_impact': self.environmental_impact,
            'sector_breakdown': self.get_sector_breakdown(),
            'confidence_score': self.confidence_score,
            'sentiment_score': self.sentiment_score,
            'sentiment_confidence': self.sentiment_confidence,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class HistoricalPolicy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    year_implemented = db.Column(db.Integer, nullable=False)
    
    # Actual outcomes
    actual_gdp_impact = db.Column(db.Float)
    actual_inflation_impact = db.Column(db.Float)
    actual_unemployment_impact = db.Column(db.Float)
    actual_environmental_impact = db.Column(db.Float)
    
    description = db.Column(Text)
    source = db.Column(db.String(500))  # Data source URL
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'sector': self.sector,
            'year_implemented': self.year_implemented,
            'actual_gdp_impact': self.actual_gdp_impact,
            'actual_inflation_impact': self.actual_inflation_impact,
            'actual_unemployment_impact': self.actual_unemployment_impact,
            'actual_environmental_impact': self.actual_environmental_impact,
            'description': self.description,
            'source': self.source
        }
