import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from data.economic_data import INDIAN_BASELINES, REGIONAL_INDICATORS, INDIAN_STATE_DATA
import logging
import random

class PolicyImpactPredictor:
    """
    Machine Learning model for predicting policy impacts on economic indicators
    """
    
    def __init__(self):
        self.gdp_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.inflation_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.unemployment_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.environmental_model = LinearRegression()
        self.scaler = StandardScaler()
        
        # Sector impact multipliers (based on economic theory)
        self.sector_multipliers = {
            'Energy': {'gdp': 1.2, 'inflation': 1.5, 'unemployment': 0.8, 'environment': 2.0},
            'Healthcare': {'gdp': 0.8, 'inflation': 0.6, 'unemployment': 1.2, 'environment': 0.3},
            'Education': {'gdp': 1.0, 'inflation': 0.4, 'unemployment': 1.0, 'environment': 0.2},
            'Transportation': {'gdp': 1.1, 'inflation': 1.2, 'unemployment': 0.9, 'environment': 1.8},
            'Agriculture': {'gdp': 0.9, 'inflation': 1.3, 'unemployment': 1.1, 'environment': 1.5},
            'Finance': {'gdp': 1.4, 'inflation': 0.8, 'unemployment': 0.7, 'environment': 0.1},
            'Technology': {'gdp': 1.5, 'inflation': 0.5, 'unemployment': 0.6, 'environment': 0.4},
            'Manufacturing': {'gdp': 1.3, 'inflation': 1.0, 'unemployment': 1.0, 'environment': 1.6}
        }
        
        # Indian regional economic sensitivity factors
        self.region_factors = {
            'Northern India': {'stability': 0.9, 'growth_potential': 1.1},
            'Western India': {'stability': 1.0, 'growth_potential': 1.3},
            'Southern India': {'stability': 1.1, 'growth_potential': 1.2},
            'Eastern India': {'stability': 0.8, 'growth_potential': 0.9},
            'North-Eastern India': {'stability': 0.7, 'growth_potential': 1.0},
            'Central India': {'stability': 0.9, 'growth_potential': 1.0}
        }
        
        self._train_models()
    
    def _train_models(self):
        """
        Train the ML models using synthetic training data based on economic principles
        """
        try:
            # Generate training data based on economic theory
            training_data = self._generate_training_data()
            
            X = training_data[['numeric_change', 'time_period', 'sector_encoded', 'region_encoded']]
            
            # Train individual models
            self.gdp_model.fit(X, training_data['gdp_impact'])
            self.inflation_model.fit(X, training_data['inflation_impact'])
            self.unemployment_model.fit(X, training_data['unemployment_impact'])
            self.environmental_model.fit(X, training_data['environmental_impact'])
            
            logging.info("ML models trained successfully")
            
        except Exception as e:
            logging.error(f"Error training models: {str(e)}")
    
    def _generate_training_data(self, n_samples=1000):
        """
        Generate synthetic training data based on economic principles and relationships
        """
        sectors = list(self.sector_multipliers.keys())
        regions = list(self.region_factors.keys())
        
        data = []
        
        for _ in range(n_samples):
            sector = random.choice(sectors)
            region = random.choice(regions)
            numeric_change = random.uniform(-50, 50)  # -50% to +50% policy change
            time_period = random.randint(1, 60)  # 1 to 60 months
            
            # Economic impact calculations based on theory
            sector_mult = self.sector_multipliers[sector]
            region_fact = self.region_factors[region]
            
            # GDP Impact: Depends on sector multiplier and magnitude of change
            gdp_base = numeric_change * 0.1 * sector_mult['gdp']
            gdp_impact = gdp_base * (1 + region_fact['growth_potential'] - 1) * 0.5
            gdp_impact += random.gauss(0, 0.2)  # Add noise
            
            # Inflation Impact: Often inverse relationship with some policies
            inflation_base = abs(numeric_change) * 0.05 * sector_mult['inflation']
            if sector in ['Energy', 'Transportation']:
                inflation_base *= 1.5  # Energy policies strongly affect inflation
            inflation_impact = inflation_base * region_fact['stability']
            inflation_impact += random.gauss(0, 0.15)
            
            # Unemployment Impact: Complex relationship
            unemployment_base = -numeric_change * 0.08 * sector_mult['unemployment']
            if numeric_change > 0:  # Policy expansion
                unemployment_base *= -0.8  # Generally reduces unemployment
            unemployment_impact = unemployment_base * region_fact['stability']
            unemployment_impact += random.gauss(0, 0.3)
            
            # Environmental Impact: Sector-dependent
            env_base = numeric_change * 0.15 * sector_mult['environment']
            if sector in ['Energy', 'Transportation', 'Manufacturing']:
                env_base *= 1.8
            environmental_impact = env_base + random.gauss(0, 0.25)
            
            data.append({
                'numeric_change': numeric_change,
                'time_period': time_period,
                'sector_encoded': sectors.index(sector),
                'region_encoded': regions.index(region),
                'gdp_impact': gdp_impact,
                'inflation_impact': inflation_impact,
                'unemployment_impact': unemployment_impact,
                'environmental_impact': environmental_impact,
                'sector': sector,
                'region': region
            })
        
        return pd.DataFrame(data)
    
    def predict_impact(self, sector, numeric_change, time_period, region):
        """
        Predict policy impacts using trained ML models
        """
        try:
            sectors = list(self.sector_multipliers.keys())
            regions = list(self.region_factors.keys())
            
            # Encode categorical variables
            sector_encoded = sectors.index(sector) if sector in sectors else 0
            region_encoded = regions.index(region) if region in regions else 0
            
            # Prepare input features
            X = np.array([[numeric_change, time_period, sector_encoded, region_encoded]])
            
            # Make predictions
            gdp_impact = self.gdp_model.predict(X)[0]
            inflation_impact = self.inflation_model.predict(X)[0]
            unemployment_impact = self.unemployment_model.predict(X)[0]
            environmental_impact = self.environmental_model.predict(X)[0]
            
            # Calculate confidence score based on input certainty
            confidence = self._calculate_confidence(sector, numeric_change, time_period)
            
            # Generate sector-wise breakdown
            sector_breakdown = self._generate_sector_breakdown(
                sector, gdp_impact, inflation_impact, unemployment_impact
            )
            
            # Simple sentiment analysis (placeholder - could be enhanced with NLP)
            sentiment_score = self._estimate_sentiment(gdp_impact, unemployment_impact, inflation_impact)
            
            return {
                'gdp_impact': round(gdp_impact, 2),
                'inflation_impact': round(inflation_impact, 2),
                'unemployment_impact': round(unemployment_impact, 2),
                'environmental_impact': round(environmental_impact, 2),
                'confidence_score': round(confidence, 2),
                'sentiment_score': round(sentiment_score, 2),
                'sentiment_confidence': 0.7,  # Placeholder
                'sector_breakdown': sector_breakdown
            }
            
        except Exception as e:
            logging.error(f"Error in prediction: {str(e)}")
            return self._get_default_prediction()
    
    def _calculate_confidence(self, sector, numeric_change, time_period):
        """Calculate prediction confidence based on input parameters"""
        confidence = 0.8  # Base confidence
        
        # Reduce confidence for extreme changes
        if abs(numeric_change) > 30:
            confidence -= 0.2
        
        # Reduce confidence for very long time periods (harder to predict)
        if time_period > 36:
            confidence -= 0.15
        
        # Adjust based on sector (some sectors are more predictable)
        if sector in ['Finance', 'Technology']:
            confidence += 0.1
        elif sector in ['Agriculture', 'Energy']:
            confidence -= 0.1
        
        return max(0.3, min(1.0, confidence))
    
    def _generate_sector_breakdown(self, primary_sector, gdp_impact, inflation_impact, unemployment_impact):
        """Generate breakdown of impacts across different sectors"""
        sectors = ['Energy', 'Healthcare', 'Education', 'Transportation', 'Agriculture', 'Finance', 'Technology', 'Manufacturing']
        
        breakdown = {}
        total_impact = abs(gdp_impact) + abs(inflation_impact) + abs(unemployment_impact)
        
        for sector in sectors:
            if sector == primary_sector:
                # Primary sector gets 40-60% of the impact
                impact_share = 0.5 + random.uniform(-0.1, 0.1)
            else:
                # Other sectors share the remaining impact based on interconnectedness
                interconnect = self._get_sector_interconnectedness(primary_sector, sector)
                impact_share = interconnect * 0.1 + random.uniform(0, 0.05)
            
            breakdown[sector] = {
                'gdp_impact': round(gdp_impact * impact_share, 2),
                'employment_impact': round(unemployment_impact * impact_share * -1, 2),
                'impact_percentage': round(impact_share * 100, 1)
            }
        
        return breakdown
    
    def _get_sector_interconnectedness(self, sector1, sector2):
        """Calculate interconnectedness between sectors (simplified)"""
        interconnections = {
            ('Energy', 'Transportation'): 0.8,
            ('Energy', 'Manufacturing'): 0.7,
            ('Technology', 'Finance'): 0.6,
            ('Healthcare', 'Education'): 0.4,
            ('Agriculture', 'Manufacturing'): 0.5,
        }
        
        # Check both directions
        return interconnections.get((sector1, sector2), 
                                  interconnections.get((sector2, sector1), 0.2))
    
    def _estimate_sentiment(self, gdp_impact, unemployment_impact, inflation_impact):
        """Simple sentiment estimation based on economic indicators"""
        sentiment = 0
        
        # Positive GDP impact increases sentiment
        sentiment += gdp_impact * 0.3
        
        # Lower unemployment increases sentiment
        sentiment -= unemployment_impact * 0.4
        
        # Lower inflation increases sentiment
        sentiment -= inflation_impact * 0.3
        
        # Add some randomness for realism
        sentiment += random.gauss(0, 0.1)
        
        # Normalize to -1 to 1 range
        return max(-1, min(1, sentiment))
    
    def _get_default_prediction(self):
        """Return default prediction in case of errors"""
        return {
            'gdp_impact': 0.0,
            'inflation_impact': 0.0,
            'unemployment_impact': 0.0,
            'environmental_impact': 0.0,
            'confidence_score': 0.5,
            'sentiment_score': 0.0,
            'sentiment_confidence': 0.5,
            'sector_breakdown': {}
        }
