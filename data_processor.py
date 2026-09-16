from app import db
from models import HistoricalPolicy
import logging

def load_historical_data():
    """
    Load sample historical policy data for comparison and training
    """
    try:
        # Check if data already exists
        existing_count = HistoricalPolicy.query.count()
        if existing_count > 0:
            logging.info(f"Historical data already exists ({existing_count} records)")
            return
        
        # Sample historical Indian policies based on real economic events
        historical_policies = [
            {
                'name': 'Goods and Services Tax (GST) Implementation',
                'country': 'India',
                'sector': 'Finance',
                'year_implemented': 2017,
                'actual_gdp_impact': 1.8,
                'actual_inflation_impact': 0.4,
                'actual_unemployment_impact': -0.8,
                'actual_environmental_impact': 0.2,
                'description': 'Unified indirect tax system replacing multiple state and central taxes',
                'source': 'Ministry of Finance, Government of India'
            },
            {
                'name': 'Renewable Energy Mission (Solar)',
                'country': 'India',
                'sector': 'Energy',
                'year_implemented': 2015,
                'actual_gdp_impact': 2.3,
                'actual_inflation_impact': -0.2,
                'actual_unemployment_impact': -1.5,
                'actual_environmental_impact': -12.8,
                'description': 'National Solar Mission to achieve 100 GW solar capacity',
                'source': 'Ministry of New and Renewable Energy'
            },
            {
                'name': 'Ayushman Bharat - Health Insurance Scheme',
                'country': 'India',
                'sector': 'Healthcare',
                'year_implemented': 2018,
                'actual_gdp_impact': 1.1,
                'actual_inflation_impact': 0.3,
                'actual_unemployment_impact': -0.7,
                'actual_environmental_impact': 0.1,
                'description': 'World\'s largest health insurance scheme covering 500 million people',
                'source': 'National Health Authority'
            },
            {
                'name': 'Digital India Initiative',
                'country': 'India',
                'sector': 'Technology',
                'year_implemented': 2015,
                'actual_gdp_impact': 2.8,
                'actual_inflation_impact': -0.1,
                'actual_unemployment_impact': -1.2,
                'actual_environmental_impact': -0.8,
                'description': 'Digital transformation program to connect rural areas',
                'source': 'Ministry of Electronics & IT'
            },
            {
                'name': 'Make in India Manufacturing Policy',
                'country': 'India',
                'sector': 'Manufacturing',
                'year_implemented': 2014,
                'actual_gdp_impact': 3.2,
                'actual_inflation_impact': 0.6,
                'actual_unemployment_impact': -2.1,
                'actual_environmental_impact': 1.2,
                'description': 'Initiative to encourage companies to manufacture products in India',
                'source': 'Department for Promotion of Industry and Internal Trade'
            },
            {
                'name': 'Pradhan Mantri Awas Yojana (Housing for All)',
                'country': 'India',
                'sector': 'Infrastructure',
                'year_implemented': 2015,
                'actual_gdp_impact': 2.1,
                'actual_inflation_impact': 0.5,
                'actual_unemployment_impact': -1.8,
                'actual_environmental_impact': 0.8,
                'description': 'Affordable housing scheme for urban and rural poor',
                'source': 'Ministry of Housing and Urban Affairs'
            },
            {
                'name': 'Jan Aushadhi Scheme (Affordable Medicines)',
                'country': 'India',
                'sector': 'Healthcare',
                'year_implemented': 2016,
                'actual_gdp_impact': 0.9,
                'actual_inflation_impact': -0.3,
                'actual_unemployment_impact': -0.4,
                'actual_environmental_impact': 0.1,
                'description': 'Generic medicines availability at affordable prices',
                'source': 'Department of Pharmaceuticals'
            },
            {
                'name': 'Skill India Mission',
                'country': 'India',
                'sector': 'Education',
                'year_implemented': 2015,
                'actual_gdp_impact': 1.7,
                'actual_inflation_impact': 0.2,
                'actual_unemployment_impact': -1.5,
                'actual_environmental_impact': 0.0,
                'description': 'Skill development and vocational training program',
                'source': 'Ministry of Skill Development and Entrepreneurship'
            },
            {
                'name': 'National Rural Employment Guarantee Act Extension',
                'country': 'India',
                'sector': 'Agriculture',
                'year_implemented': 2020,
                'actual_gdp_impact': 1.3,
                'actual_inflation_impact': 0.4,
                'actual_unemployment_impact': -2.8,
                'actual_environmental_impact': -0.5,
                'description': 'Enhanced rural employment guarantee scheme during COVID-19',
                'source': 'Ministry of Education'
            },
            {
                'name': 'Agricultural Subsidies Reform',
                'country': 'India',
                'sector': 'Agriculture',
                'year_implemented': 2021,
                'actual_gdp_impact': 0.6,
                'actual_inflation_impact': -0.3,
                'actual_unemployment_impact': 0.4,
                'actual_environmental_impact': -1.2,
                'description': 'Reform of agricultural support and subsidy programs',
                'source': 'Ministry of Agriculture and Farmers Welfare'
            },
            {
                'name': 'High-Speed Rail Investment',
                'country': 'Japan',
                'sector': 'Transportation',
                'year_implemented': 2016,
                'actual_gdp_impact': 1.8,
                'actual_inflation_impact': 0.2,
                'actual_unemployment_impact': -0.7,
                'actual_environmental_impact': -3.5,
                'description': 'Major infrastructure investment in rail transportation',
                'source': 'Ministry of Land, Infrastructure, Transport and Tourism'
            },
            {
                'name': 'Tech Industry Tax Incentives',
                'country': 'Ireland',
                'sector': 'Technology',
                'year_implemented': 2017,
                'actual_gdp_impact': 3.2,
                'actual_inflation_impact': 0.5,
                'actual_unemployment_impact': -1.2,
                'actual_environmental_impact': -0.8,
                'description': 'Tax incentives to attract technology companies',
                'source': 'Department of Finance'
            },
            {
                'name': 'Manufacturing Revival Plan',
                'country': 'Germany',
                'sector': 'Manufacturing',
                'year_implemented': 2018,
                'actual_gdp_impact': 2.1,
                'actual_inflation_impact': 0.6,
                'actual_unemployment_impact': -0.9,
                'actual_environmental_impact': 2.3,
                'description': 'Industry 4.0 initiative to modernize manufacturing',
                'source': 'Federal Ministry for Economic Affairs and Energy'
            },
            {
                'name': 'Renewable Energy Transition',
                'country': 'Denmark',
                'sector': 'Energy',
                'year_implemented': 2019,
                'actual_gdp_impact': 1.5,
                'actual_inflation_impact': 0.3,
                'actual_unemployment_impact': -0.4,
                'actual_environmental_impact': -12.8,
                'description': 'Accelerated transition to renewable energy sources',
                'source': 'Danish Energy Agency'
            },
            {
                'name': 'Universal Basic Income Pilot',
                'country': 'Finland',
                'sector': 'Finance',
                'year_implemented': 2017,
                'actual_gdp_impact': 0.4,
                'actual_inflation_impact': 0.2,
                'actual_unemployment_impact': -0.6,
                'actual_environmental_impact': 0.0,
                'description': 'Two-year pilot program for unconditional basic income',
                'source': 'Social Insurance Institution of Finland'
            },
            {
                'name': 'Smart City Infrastructure',
                'country': 'Singapore',
                'sector': 'Technology',
                'year_implemented': 2020,
                'actual_gdp_impact': 2.3,
                'actual_inflation_impact': 0.4,
                'actual_unemployment_impact': -0.8,
                'actual_environmental_impact': -2.1,
                'description': 'Comprehensive smart city technology implementation',
                'source': 'Smart Nation and Digital Government Office'
            }
        ]
        
        # Insert historical policies into database
        for policy_data in historical_policies:
            policy = HistoricalPolicy(**policy_data)
            db.session.add(policy)
        
        db.session.commit()
        logging.info(f"Successfully loaded {len(historical_policies)} historical policies")
        
    except Exception as e:
        logging.error(f"Error loading historical data: {str(e)}")
        db.session.rollback()
        raise e

def validate_policy_input(policy_data):
    """
    Validate policy input data
    """
    required_fields = ['name', 'sector', 'region', 'numeric_change', 'time_period']
    
    for field in required_fields:
        if field not in policy_data or policy_data[field] is None:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate numeric ranges
    if not -100 <= policy_data['numeric_change'] <= 100:
        raise ValueError("Numeric change must be between -100% and 100%")
    
    if not 1 <= policy_data['time_period'] <= 120:
        raise ValueError("Time period must be between 1 and 120 months")
    
    # Validate sector
    valid_sectors = ['Energy', 'Healthcare', 'Education', 'Transportation', 
                    'Agriculture', 'Finance', 'Technology', 'Manufacturing']
    if policy_data['sector'] not in valid_sectors:
        raise ValueError(f"Invalid sector. Must be one of: {', '.join(valid_sectors)}")
    
    # Validate region
    valid_regions = ['North America', 'Europe', 'Asia', 'Africa', 'South America', 'Oceania']
    if policy_data['region'] not in valid_regions:
        raise ValueError(f"Invalid region. Must be one of: {', '.join(valid_regions)}")
    
    return True

def calculate_economic_multipliers(sector, region):
    """
    Calculate economic multipliers based on sector and region
    """
    sector_multipliers = {
        'Energy': 1.2,
        'Healthcare': 0.8,
        'Education': 1.0,
        'Transportation': 1.1,
        'Agriculture': 0.9,
        'Finance': 1.4,
        'Technology': 1.5,
        'Manufacturing': 1.3
    }
    
    region_adjustments = {
        'North America': 1.0,
        'Europe': 0.9,
        'Asia': 1.2,
        'Africa': 1.1,
        'South America': 1.0,
        'Oceania': 0.8
    }
    
    base_multiplier = sector_multipliers.get(sector, 1.0)
    region_adjustment = region_adjustments.get(region, 1.0)
    
    return base_multiplier * region_adjustment

def format_prediction_results(prediction):
    """
    Format prediction results for display
    """
    return {
        'gdp': {
            'value': prediction.gdp_impact,
            'formatted': f"{prediction.gdp_impact:+.2f}%",
            'interpretation': _get_gdp_interpretation(prediction.gdp_impact)
        },
        'inflation': {
            'value': prediction.inflation_impact,
            'formatted': f"{prediction.inflation_impact:+.2f} pp",
            'interpretation': _get_inflation_interpretation(prediction.inflation_impact)
        },
        'unemployment': {
            'value': prediction.unemployment_impact,
            'formatted': f"{prediction.unemployment_impact:+.2f} pp",
            'interpretation': _get_unemployment_interpretation(prediction.unemployment_impact)
        },
        'environment': {
            'value': prediction.environmental_impact,
            'formatted': f"{prediction.environmental_impact:+.2f}%",
            'interpretation': _get_environment_interpretation(prediction.environmental_impact)
        }
    }

def _get_gdp_interpretation(value):
    if value > 1:
        return "Strong positive impact"
    elif value > 0:
        return "Positive impact"
    elif value > -1:
        return "Minimal impact"
    else:
        return "Negative impact"

def _get_inflation_interpretation(value):
    if value > 0.5:
        return "Inflationary pressure"
    elif value > -0.5:
        return "Stable inflation"
    else:
        return "Deflationary pressure"

def _get_unemployment_interpretation(value):
    if value > 0.5:
        return "Job losses expected"
    elif value > -0.5:
        return "Stable employment"
    else:
        return "Job creation expected"

def _get_environment_interpretation(value):
    if value > 2:
        return "Environmental concern"
    elif value > -2:
        return "Neutral impact"
    else:
        return "Environmental benefit"
